import cv2
import torch
import numpy as np
from torchvision import transforms
import torch.nn.functional as F
import facenet_pytorch
from PIL import Image
from ultralytics import YOLO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Running on: {device}")

face_detector = facenet_pytorch.MTCNN(thresholds=[0.6, 0.7, 0.7], keep_all=True, device=device, min_face_size=10)
resnet = facenet_pytorch.InceptionResnetV1(pretrained='vggface2').eval().to(device)
preprocess = transforms.Compose([
    transforms.ToPILImage(), transforms.Resize((160, 160)),
    transforms.ToTensor(), transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])
yolo_model = YOLO('yolov8n.pt')

def get_raw_face(img_rgb, box):
    x1, y1, x2, y2 = box.astype(int)
    w, h = x2 - x1, y2 - y1
    x, y = max(0, x1), max(0, y1)
    face_crop = img_rgb[y:y+h, x:x+w]
    if face_crop.size == 0: return None
    return face_crop

target_image_path = 'C:/Users/rajti/Downloads/messi1.jpg'
img = Image.open(target_image_path).convert('RGB')
img_rgb = np.array(img)

boxes, probs = face_detector.detect(img_rgb)
biggest_box = max(boxes, key=lambda b: (b[2]-b[0]) * (b[3]-b[1]))
perfect_face = get_raw_face(img_rgb, biggest_box)
tensor = preprocess(perfect_face).unsqueeze(0).to(device)
with torch.no_grad():
    master_embedding = resnet(tensor)

video_path = 'C:/Users/rajti/Downloads/messivideo.mp4'
cap = cv2.VideoCapture(video_path)

TARGET_TRACK_ID = None
known_non_targets = set()
COSINE_THRESHOLD = 0.30

results = yolo_model.track(source=video_path, classes=[0], stream=True, persist=True, verbose=False)

frame_num = 0
for r in results:
    frame_num += 1
    frame_bgr = r.orig_img
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    
    if r.boxes.id is not None:
        boxes = r.boxes.xyxy.cpu().numpy()
        track_ids = r.boxes.id.cpu().numpy().astype(int)
        
        for box, track_id in zip(boxes, track_ids):
            if track_id in known_non_targets or track_id == TARGET_TRACK_ID:
                continue
                
            x1, y1, x2, y2 = box.astype(int)
            x, y = max(0, x1), max(0, y1)
            w, h = x2 - x1, y2 - y1
            
            # EXPAND THE YOLO BOX SLIGHTLY TO ENSURE HEAD IS INCLUDED
            expand_ratio = 0.2
            y_exp = max(0, int(y - h * expand_ratio))
            body_crop = frame_rgb[y_exp:y+h, x:x+w]
            if body_crop.size == 0: continue
            
            face_boxes, probs = face_detector.detect(body_crop)
            if face_boxes is not None and len(face_boxes) > 0:
                print(f"Frame {frame_num}: Found {len(face_boxes)} faces in Body #{track_id}")
                biggest_face = max(face_boxes, key=lambda b: (b[2]-b[0]) * (b[3]-b[1]))
                perfect_face = get_raw_face(body_crop, biggest_face)
                if perfect_face is not None:
                    with torch.no_grad():
                        tensor = preprocess(perfect_face).unsqueeze(0).to(device)
                        embedding = resnet(tensor)
                    
                    cosine_sim = F.cosine_similarity(master_embedding, embedding).item()
                    print(f"Frame {frame_num}: Body #{track_id} Cosine Sim vs Messi = {cosine_sim:.2f}")
                    if cosine_sim > COSINE_THRESHOLD:
                        TARGET_TRACK_ID = track_id
                    else:
                        known_non_targets.add(track_id)
            else:
                # No face detected in this crop
                pass

cap.release()
print(f"Final Target ID: {TARGET_TRACK_ID}")
