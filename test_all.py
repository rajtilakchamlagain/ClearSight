import cv2
import numpy as np
from ultralytics import YOLO
import insightface
from insightface.app import FaceAnalysis
import os

print("Loading models...")
yolo_model = YOLO('yolov8n.pt') 
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

def cosine_sim(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return np.dot(a, b)

def test_video(name, vid_path, ref_path):
    print(f"\n==========================================")
    print(f"Testing {name}")
    print(f"==========================================")
    
    img = cv2.imread(ref_path)
    faces = face_app.get(img)
    if not faces:
        print(f"Error: No face detected in reference image {ref_path}")
        return
        
    biggest_face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
    master_vector = biggest_face.embedding
    master_vector = master_vector / np.linalg.norm(master_vector)

    tracklets = {}
    results = yolo_model.track(source=vid_path, classes=[0], stream=True, persist=True, verbose=False, tracker="bytetrack.yaml")
    
    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frame_idx = 0
    for r in results:
        frame_bgr = r.orig_img
        
        # Run face detection whenever YOLO detects a person in the frame to maximize embedding quality
        if r.boxes.id is not None and len(r.boxes.id) > 0:
            faces_in_frame = face_app.get(frame_bgr)
            boxes = r.boxes.xyxy.cpu().numpy()
            track_ids = r.boxes.id.cpu().numpy().astype(int)
            
            for box, track_id in zip(boxes, track_ids):
                if track_id not in tracklets:
                    tracklets[track_id] = {'embeddings_gallery': [], 'boxes': {}}
                
                tracklets[track_id]['boxes'][frame_idx] = box
                
                x1, y1, x2, y2 = box.astype(int)
                for face in faces_in_frame:
                    fx1, fy1, fx2, fy2 = face.bbox
                    fcx, fcy = (fx1+fx2)/2, (fy1+fy2)/2
                    
                    # Ensure facial midpoint lies comfortably inside person bounding box
                    if x1 <= fcx <= x2 and y1 <= fcy <= y2:
                        face_area = (fx2-fx1) * (fy2-fy1)
                        face_img = frame_bgr[max(0, int(fy1)):max(0, int(fy2)), max(0, int(fx1)):max(0, int(fx2))].copy()
                        tracklets[track_id]['embeddings_gallery'].append((face_area, face.embedding, face_img))
        frame_idx += 1
        print(f"\rTracking... Frame {frame_idx}/{total_frames}", end="")
    print()

    # Phase 2: Enterprise Dynamic Tracklet Clustering (Multi-Embedding Gallery)
    TARGET_IDS = set()
    if tracklets:
        master_scores = {}
        for track_id, data in tracklets.items():
            gallery = data['embeddings_gallery']
            if gallery:
                sims = [cosine_sim(master_vector, emb) for _, emb, _ in gallery]
                max_sim = max(sims)
                master_scores[track_id] = max_sim
                if max_sim > 0.15:
                    print(f"  [Track #{track_id}] Max Sim vs Master (from {len(gallery)} faces): {max_sim:.4f}")
        
        if master_scores:
            best_id = max(master_scores, key=master_scores.get)
            s_max = master_scores[best_id]
            print(f"  --> Primary Anchor Matched: Track #{best_id} (Score: {s_max:.4f})")
            
            # Floor check: If the highest confidence match in the entire footage is < 0.15, no target present.
            if s_max >= 0.15:
                TARGET_IDS.add(best_id)
                
                # Dynamic Threshold Calculation: scale relative to anchor quality with a flexible floor
                dynamic_threshold = max(s_max * 0.65, 0.18)
                print(f"  --> Dynamic Auto-Threshold set to: {dynamic_threshold:.4f} (65% of anchor or 0.18 floor)")
                
                # Iterative Tracklet Clustering across galleries
                added_new = True
                while added_new:
                    added_new = False
                    for candidate_id, data in tracklets.items():
                        if candidate_id not in TARGET_IDS and data['embeddings_gallery']:
                            cand_gallery = data['embeddings_gallery']
                            
                            # Max similarity against master reference OR any confirmed target's faces
                            sim_to_master = max(cosine_sim(master_vector, emb) for _, emb, _ in cand_gallery)
                            sim_to_cluster = 0.0
                            for ver_id in TARGET_IDS:
                                ver_gallery = tracklets[ver_id]['embeddings_gallery']
                                # Quick comparison against top 5 largest faces of verified tracklet to save time
                                top_ver = sorted(ver_gallery, key=lambda x: x[0], reverse=True)[:5]
                                m_sim = max(cosine_sim(c_emb, v_emb) for _, c_emb, _ in cand_gallery for _, v_emb, _ in top_ver)
                                if m_sim > sim_to_cluster:
                                    sim_to_cluster = m_sim
                                    
                            best_sim = max(sim_to_master, sim_to_cluster)
                            if best_sim >= dynamic_threshold:
                                print(f"  --> ReID Linked Track #{candidate_id} into cluster (Sim: {best_sim:.4f} >= {dynamic_threshold:.4f})")
                                TARGET_IDS.add(candidate_id)
                                added_new = True
            else:
                print(f"  --> No confident target found (Best similarity {s_max:.4f} is below 0.15 floor).")
                        
    if not TARGET_IDS:
        print("FAILED to find any target tracklets.")
        return
        
    print(f"Target locked onto IDs: {TARGET_IDS}")
    
    target_frames = {}
    for tid in TARGET_IDS:
        for f_idx, box in tracklets[tid]['boxes'].items():
            target_frames[f_idx] = box
            
    # Phase 3: Bounded Occlusion Interpolation
    sorted_f_idxs = sorted(target_frames.keys())
    interpolated_frames = target_frames.copy()
    MAX_GAP = max(int(fps * 3.5), 90)  # Max ~3.5 seconds occlusion tolerance
    
    for i in range(len(sorted_f_idxs) - 1):
        f1 = sorted_f_idxs[i]
        f2 = sorted_f_idxs[i+1]
        gap = f2 - f1
        
        if 1 < gap <= MAX_GAP:
            box1 = np.array(target_frames[f1])
            box2 = np.array(target_frames[f2])
            for j in range(1, gap):
                f_curr = f1 + j
                alpha = j / gap
                box_curr = (1 - alpha) * box1 + alpha * box2
                interpolated_frames[f_curr] = box_curr
    
    print(f"Original frames tracked: {len(target_frames)}")
    print(f"Total frames tracked after Interpolation: {len(interpolated_frames)}")
    coverage = (len(interpolated_frames) / total_frames) * 100
    print(f"Tracking Coverage: {coverage:.2f}% of the entire video!")

tests = [
    ("Hank (Catch Me If You Can)", r"Test\TomHank_Cropped_Fixed.mp4", r"Test\hank1.jpg"),
    ("Messi", r"Test\messivideo.mp4", r"Test\messi1.jpg"),
    ("SRK", r"Test\srkvideo.mp4", r"Test\srk2.jpg")
]

for name, vid, ref in tests:
    test_video(name, vid, ref)
