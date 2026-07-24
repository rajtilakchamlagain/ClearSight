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
        if frame_idx % 3 == 0:
            faces_in_frame = face_app.get(frame_bgr)
        else:
            faces_in_frame = []
            
        if r.boxes.id is not None:
            boxes = r.boxes.xyxy.cpu().numpy()
            track_ids = r.boxes.id.cpu().numpy().astype(int)
            
            for box, track_id in zip(boxes, track_ids):
                if track_id not in tracklets:
                    tracklets[track_id] = {'max_face_size': 0, 'best_face_img': None, 'best_face_embedding': None, 'boxes': {}}
                
                tracklets[track_id]['boxes'][frame_idx] = box
                
                x1, y1, x2, y2 = box.astype(int)
                for face in faces_in_frame:
                    fx1, fy1, fx2, fy2 = face.bbox
                    fcx, fcy = (fx1+fx2)/2, (fy1+fy2)/2
                    
                    if x1 <= fcx <= x2 and (y1 - (y2-y1)*0.2) <= fcy <= y2:
                        face_area = (fx2-fx1) * (fy2-fy1)
                        if face_area > tracklets[track_id]['max_face_size']:
                            tracklets[track_id]['max_face_size'] = face_area
                            tracklets[track_id]['best_face_img'] = frame_bgr[max(0, int(fy1)):max(0, int(fy2)), max(0, int(fx1)):max(0, int(fx2))].copy()
                            tracklets[track_id]['best_face_embedding'] = face.embedding
        frame_idx += 1
        print(f"\rTracking... Frame {frame_idx}/{total_frames}", end="")
    print()

    TARGET_IDS = set()
    if tracklets:
        scores = {}
        for track_id, data in tracklets.items():
            if data.get('best_face_embedding') is not None:
                scores[track_id] = cosine_sim(master_vector, data['best_face_embedding'])
        
        if scores:
            best_id = max(scores, key=scores.get)
            TARGET_IDS.add(best_id)
            video_anchor_vector = tracklets[best_id]['best_face_embedding']
            
            for track_id, data in tracklets.items():
                if track_id != best_id and data.get('best_face_embedding') is not None:
                    anchor_score = cosine_sim(video_anchor_vector, data['best_face_embedding'])
                    print(f"Track {track_id} vs Anchor: {anchor_score:.3f}")
                    if anchor_score >= 0.35: # Lowered to see what's passing
                        TARGET_IDS.add(track_id)
                        
    if not TARGET_IDS:
        print("FAILED to find any target tracklets.")
        return
        
    print(f"Target locked onto IDs: {TARGET_IDS}")
    
    target_frames = {}
    for tid in TARGET_IDS:
        for f_idx, box in tracklets[tid]['boxes'].items():
            target_frames[f_idx] = box
            
    # Interpolation
    sorted_f_idxs = sorted(target_frames.keys())
    interpolated_frames = target_frames.copy()
    for i in range(len(sorted_f_idxs) - 1):
        f1 = sorted_f_idxs[i]
        f2 = sorted_f_idxs[i+1]
        gap = f2 - f1
        
        if 1 < gap: # No MAX_GAP limit
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
