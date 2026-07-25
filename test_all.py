import ssl
try:
    ssl._create_default_https_context = ssl._create_unverified_context
    ssl.create_default_context = ssl._create_unverified_context
except AttributeError:
    pass

import cv2
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from ultralytics import YOLO
import insightface
from insightface.app import FaceAnalysis
import os

print("Loading industrial AI surveillance models...")
yolo_model = YOLO('yolov8n.pt') 
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

# Initialize Deep Whole-Body Feature Extractor (Translation-invariant deep visual appearance vector)
body_embedder = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
body_embedder.classifier = torch.nn.Identity() # Remove classification head to extract pure 576D feature vector
body_embedder.eval()

body_transform = transforms.Compose([
    transforms.Resize((256, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def extract_body_embedding(img_bgr):
    try:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        tensor_img = body_transform(pil_img).unsqueeze(0)
        with torch.no_grad():
            vec = body_embedder(tensor_img).numpy().flatten()
        return vec / (np.linalg.norm(vec) + 1e-6)
    except Exception:
        return np.zeros(576)

def extract_apparel_signature(img_bgr):
    """Computes spatial upper/lower body HSV apparel signature invariant to camera orientation."""
    try:
        h, w = img_bgr.shape[:2]
        if h < 20 or w < 10:
            return np.zeros(96)
            
        # Center-Crop Inner Torso Core (width 25% to 75%) to reject background crowds and lighting
        x1, x2 = int(w * 0.25), int(w * 0.75)
        core_bgr = img_bgr[:, x1:x2] if (x2 > x1 + 4) else img_bgr
        
        upper_img = core_bgr[int(h*0.15):int(h*0.55), :] # Shirt/Jersey core
        lower_img = core_bgr[int(h*0.55):int(h*0.88), :] # Shorts/Trousers core
        
        sig = []
        for part in [upper_img, lower_img]:
            hsv = cv2.cvtColor(part, cv2.COLOR_BGR2HSV)
            hist_h = cv2.calcHist([hsv], [0], None, [16], [0, 180]).flatten()
            hist_s = cv2.calcHist([hsv], [1], None, [16], [0, 256]).flatten()
            hist_v = cv2.calcHist([hsv], [2], None, [16], [0, 256]).flatten()
            part_hist = np.concatenate([hist_h, hist_s, hist_v])
            sig.append(part_hist / (np.linalg.norm(part_hist) + 1e-6))
        return np.concatenate(sig)
    except Exception:
        return np.zeros(96)

def cosine_sim(a, b):
    if a is None or b is None:
        return 0.0
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(a / norm_a, b / norm_b)

def test_video(name, vid_path, ref_path):
    print(f"\n==========================================")
    print(f"Testing Industrial ReID: {name}")
    print(f"==========================================")
    
    ref_bgr = cv2.imread(ref_path)
    if ref_bgr is None:
        print(f"Error: Could not load reference image {ref_path}")
        return
        
    faces = face_app.get(ref_bgr)
    master_face_vec = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1])).embedding if faces else None
    if master_face_vec is not None:
        master_face_vec = master_face_vec / np.linalg.norm(master_face_vec)
        
    master_body_vec = extract_body_embedding(ref_bgr)
    master_apparel_sig = extract_apparel_signature(ref_bgr)

    tracklets = {}
    results = yolo_model.track(source=vid_path, classes=[0], stream=True, persist=True, verbose=False, tracker="bytetrack.yaml")
    
    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frame_idx = 0
    for r in results:
        frame_bgr = r.orig_img
        
        if r.boxes.id is not None and len(r.boxes.id) > 0:
            faces_in_frame = face_app.get(frame_bgr)
            boxes = r.boxes.xyxy.cpu().numpy()
            track_ids = r.boxes.id.cpu().numpy().astype(int)
            
            for box, track_id in zip(boxes, track_ids):
                if track_id not in tracklets:
                    tracklets[track_id] = {
                        'boxes': {}, 'face_gallery': [], 
                        'body_gallery': [], 'apparel_gallery': []
                    }
                
                tracklets[track_id]['boxes'][frame_idx] = box
                x1, y1, x2, y2 = box.astype(int)
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(frame_bgr.shape[1], x2), min(frame_bgr.shape[0], y2)
                
                if x2 - x1 > 10 and y2 - y1 > 20:
                    body_crop = frame_bgr[y1:y2, x1:x2]
                    # Sample body semantics and apparel every 5th frame per tracklet to keep compute lean & expressive
                    if len(tracklets[track_id]['boxes']) % 5 == 1 or len(tracklets[track_id]['body_gallery']) == 0:
                        tracklets[track_id]['body_gallery'].append(extract_body_embedding(body_crop))
                        tracklets[track_id]['apparel_gallery'].append(extract_apparel_signature(body_crop))
                
                for face in faces_in_frame:
                    fx1, fy1, fx2, fy2 = face.bbox
                    fcx, fcy = (fx1+fx2)/2, (fy1+fy2)/2
                    if x1 <= fcx <= x2 and y1 <= fcy <= y2:
                        face_area = (fx2-fx1) * (fy2-fy1)
                        tracklets[track_id]['face_gallery'].append((face_area, face.embedding))
                        
        frame_idx += 1
        print(f"\rPass 1: Deep Semantic Scanning... Frame {frame_idx}/{total_frames}", end="")
    print()

    # Phase 2: Whole-Body Person Re-Identification & Backend Pruning Engine
    TARGET_IDS = set()
    if not tracklets:
        print("FAILED: No human trajectories found.")
        return

    # 1. Calculate Hybrid ReID Scores against Reference Image
    master_scores = {}
    for tid, data in tracklets.items():
        # Discard transient noise / flickering boxes immediately in backend
        if len(data['boxes']) < 6:
            continue
            
        face_sim = max([cosine_sim(master_face_vec, emb) for _, emb in data['face_gallery']], default=0.0)
        body_sim = max([cosine_sim(master_body_vec, b_vec) for b_vec in data['body_gallery']], default=0.0)
        apparel_sim = max([cosine_sim(master_apparel_sig, a_sig) for a_sig in data['apparel_gallery']], default=0.0)
        
        # Hybrid weights: Face is decisive when visible, body + apparel bridge the gap when face is blurry/distant
        if face_sim > 0.35:
            score = 0.70 * face_sim + 0.15 * body_sim + 0.15 * apparel_sim
        else:
            score = 0.20 * max(0.0, face_sim) + 0.45 * body_sim + 0.35 * apparel_sim
            
        master_scores[tid] = (score, face_sim, body_sim, apparel_sim)

    if not master_scores:
        print("FAILED: All trajectories filtered out as transient noise.")
        return

    # 2. Lock onto Primary Target Anchor in footage
    best_id = max(master_scores, key=lambda k: master_scores[k][0])
    s_max, f_max, b_max, a_max = master_scores[best_id]
    print(f"  --> Primary Target Anchor Locked: Track #{best_id} (Hybrid Score: {s_max:.4f} | Face: {f_max:.2f}, Body: {b_max:.2f}, Apparel: {a_max:.2f})")

    if s_max < 0.22:
        print(f"  --> No confident target in video (Anchor score {s_max:.4f} below safety rejection threshold).")
        return
        
    TARGET_IDS.add(best_id)
    
    # 3. Whole-Body ReID with Forensic Biometric Veto & Temporal Exclusion (Industrial Standard)
    anchor_frames = set(tracklets[best_id]['boxes'].keys())
    anchor_body_gallery = tracklets[best_id]['body_gallery']
    anchor_apparel_gallery = tracklets[best_id]['apparel_gallery']
    anchor_face_gallery = [emb for _, emb in tracklets[best_id]['face_gallery']]
    
    dynamic_thresh = max(s_max * 0.82, 0.65)
    print(f"  --> Strict Forensic ReID Threshold set to: {dynamic_thresh:.4f} (With Biometric Veto & No-Teleportation Law)")
    
    for candidate_id, data in tracklets.items():
        if candidate_id == best_id or len(data['boxes']) < 8: # Ignore short duration noise (< ~0.3s)
            continue
        c_score, c_face, c_body, c_apparel = master_scores.get(candidate_id, (0.0, 0.0, 0.0, 0.0))
        
        # Rule 1: FORENSIC BIOMETRIC VETO
        if len(data['face_gallery']) > 0 and c_face < 0.22:
            continue
            
        # Rule 2: SIMULTANEOUS EXISTENCE VETO (No-Teleportation Law)
        # A subject coexisting in the exact same frames as the confirmed primary anchor cannot be the target!
        cand_frames = set(data['boxes'].keys())
        if len(anchor_frames.intersection(cand_frames)) > 3:
            continue
            
        sim_to_anchor_body = max([cosine_sim(cb, ab) for cb in data['body_gallery'] for ab in anchor_body_gallery], default=0.0)
        sim_to_anchor_apparel = max([cosine_sim(ca, aa) for ca in data['apparel_gallery'] for aa in anchor_apparel_gallery], default=0.0)
        sim_to_anchor_face = max([cosine_sim(cf, af) for _, cf in data['face_gallery'] for af in anchor_face_gallery], default=0.0)
        
        if c_face >= 0.25 or sim_to_anchor_face >= 0.35:
            # Confirmed biometric facial similarity overrides everything
            anchor_match_score = 0.60 * max(c_face, sim_to_anchor_face) + 0.20 * sim_to_anchor_body + 0.20 * sim_to_anchor_apparel
            best_overall_score = max(c_score, anchor_match_score)
            if best_overall_score >= dynamic_thresh:
                print(f"  --> Verified Target ReID Track #{candidate_id} (Score: {best_overall_score:.4f} | Face Match: {max(c_face, sim_to_anchor_face):.2f})")
                TARGET_IDS.add(candidate_id)
        else:
            # Rule 3: STRICT NON-BIOMETRIC FLOOR
            # Without face visibility, require high visual body & inner garment fidelity (>= 0.75)
            anchor_match_score = 0.50 * sim_to_anchor_body + 0.50 * sim_to_anchor_apparel
            best_overall_score = max(c_score, anchor_match_score)
            if best_overall_score >= max(dynamic_thresh, 0.75) and sim_to_anchor_body >= 0.65 and sim_to_anchor_apparel >= 0.65:
                print(f"  --> Verified Target ReID Track #{candidate_id} (Score: {best_overall_score:.4f} | Body+Apparel High Correlation)")
                TARGET_IDS.add(candidate_id)

    print(f"Target locked onto validated IDs: {TARGET_IDS}")

    # Phase 3: Bounded Occlusion Interpolation & Clean Trajectory Rendering
    target_frames = {}
    for tid in TARGET_IDS:
        for f_idx, box in tracklets[tid]['boxes'].items():
            target_frames[f_idx] = box
            
    sorted_f_idxs = sorted(target_frames.keys())
    interpolated_frames = target_frames.copy()
    MAX_GAP = max(int(fps * 2.5), 60) # Tightened ~2.5 seconds occlusion tolerance to prevent jumping across players
    
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
                interpolated_frames[f_curr] = (1 - alpha) * box1 + alpha * box2

    print(f"Original validated frames tracked: {len(target_frames)}")
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
