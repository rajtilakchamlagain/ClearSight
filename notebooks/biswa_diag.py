import torch
import cv2
import numpy as np
import os
import facenet_pytorch
from torchvision import transforms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
detector = facenet_pytorch.MTCNN(thresholds=[0.7, 0.8, 0.8], keep_all=True, device=device)
resnet = facenet_pytorch.InceptionResnetV1(pretrained='vggface2').eval().to(device)
preprocess = transforms.Compose([
    transforms.ToPILImage(), transforms.Resize((160, 160)),
    transforms.ToTensor(), transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

def detect_faces_gpu(img_rgb):
    boxes, probs, landmarks = detector.detect(img_rgb, landmarks=True)
    if boxes is None: return []
    faces = []
    for i in range(len(boxes)):
        if probs[i] > 0.90:
            box = boxes[i].astype(int)
            x1, y1, x2, y2 = box
            w, h = x2 - x1, y2 - y1
            faces.append({'box': [x1, y1, w, h], 'confidence': probs[i]})
    return faces

def get_perfect_face(img_rgb, face):
    x, y, w, h = face['box']
    x, y = max(0, x), max(0, y)
    face_crop = img_rgb[y:y+h, x:x+w]
    if face_crop.size == 0: return None
    return face_crop

anchor_paths = ['../../data/biswa_face.jpeg', '../../data/biswa_face2.jpeg', '../../data/biswa_face3.jpeg']
anchor_embeddings = []
for path in anchor_paths:
    if os.path.exists(path):
        img_rgb = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        faces = detect_faces_gpu(img_rgb)
        if len(faces) > 0:
            biggest_face = max(faces, key=lambda f: f['box'][2] * f['box'][3])
            perfect_face = get_perfect_face(img_rgb, biggest_face)
            if perfect_face is not None:
                tensor = preprocess(perfect_face).unsqueeze(0).to(device)
                with torch.no_grad():
                    anchor_embeddings.append(resnet(tensor))
master_embedding = torch.mean(torch.cat(anchor_embeddings), dim=0, keepdim=True)

video_path = '../../data/test_video3.mp4'
cap = cv2.VideoCapture(video_path)
frame_count = 0
output_lines = []

while cap.isOpened():
    ret, frame_bgr = cap.read()
    if not ret: break
    frame_count += 1
    
    if frame_count % 5 != 0:
        continue 
    
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    faces = detect_faces_gpu(frame_rgb)
    for i, face in enumerate(faces):
        enhanced_rgb = get_perfect_face(frame_rgb, face)
        if enhanced_rgb is None: continue
        target_tensor = preprocess(enhanced_rgb).unsqueeze(0).to(device)
        with torch.no_grad():
            target_embedding = resnet(target_tensor)
        distance = torch.dist(master_embedding, target_embedding).item()
        
        # Only log reasonably close faces
        if distance < 1.2:
            output_lines.append(f"Frame {frame_count} | dist: {distance:.3f}")

cap.release()
with open('biswa_diag.txt', 'w') as f:
    f.write("\n".join(output_lines))
print("DIAGNOSTIC DONE")
