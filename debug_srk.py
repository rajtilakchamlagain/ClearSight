import os
import cv2
import torch
import numpy as np
from torchvision import transforms
import facenet_pytorch
from PIL import Image

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Initialize MTCNN with lower thresholds for blurry video
detector = facenet_pytorch.MTCNN(keep_all=True, min_face_size=10, thresholds=[0.6, 0.7, 0.7], device=device)
resnet = facenet_pytorch.InceptionResnetV1(pretrained='vggface2').eval().to(device)
preprocess = transforms.Compose([
    transforms.ToPILImage(), transforms.Resize((160, 160)),
    transforms.ToTensor(), transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

def get_perfect_face(img_rgb, box):
    x1, y1, x2, y2 = [int(v) for v in box]
    w, h = x2 - x1, y2 - y1
    x, y = max(0, x1), max(0, y1)
    face_crop = img_rgb[y:y+h, x:x+w]
    if face_crop.size == 0: return None
    lab = cv2.cvtColor(face_crop, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    cl = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    return cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2RGB)

print("Processing SRK reference images...")
anchor_embeddings = []
for file in ['srk1.webp', 'srk2.jpg', 'srk3.jpg', 'srk4.webp']:
    path = f'C:/Users/rajti/Downloads/{file}'
    if not os.path.exists(path): continue
    try:
        img = Image.open(path).convert('RGB')
        img_rgb = np.array(img)
        boxes, probs, _ = detector.detect(img_rgb, landmarks=True)
        if boxes is not None:
            best_idx = np.argmax(probs)
            face = get_perfect_face(img_rgb, boxes[best_idx])
            if face is not None:
                tensor = preprocess(face).unsqueeze(0).to(device)
                with torch.no_grad():
                    anchor_embeddings.append(resnet(tensor))
    except Exception as e:
        print(f"Error reading {file}: {e}")

if not anchor_embeddings:
    print("Failed to extract master vector from images.")
    exit()

master_embedding = torch.mean(torch.cat(anchor_embeddings), dim=0, keepdim=True)
print(f"Master Vector Extracted from {len(anchor_embeddings)} images.")

print("Scanning footage1.mp4...")
cap = cv2.VideoCapture('C:/Users/rajti/Downloads/footage1.mp4')
frame_count = 0
found = False

while cap.isOpened() and frame_count < 100:
    ret, frame = cap.read()
    if not ret: break
    frame_count += 1
    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, probs, _ = detector.detect(img_rgb, landmarks=True)
    
    if boxes is not None:
        for i, box in enumerate(boxes):
            if probs[i] > 0.60: # lower probability threshold
                face = get_perfect_face(img_rgb, box)
                if face is not None:
                    tensor = preprocess(face).unsqueeze(0).to(device)
                    with torch.no_grad():
                        embedding = resnet(tensor)
                    distance = torch.dist(master_embedding, embedding).item()
                    
                    # Print any face that is somewhat close to SRK
                    if distance < 1.3:
                        print(f"Frame {frame_count}: Face found with prob {probs[i]:.2f}. Distance to SRK: {distance:.3f}")
                        found = True

if not found:
    print("Could not find any faces matching SRK within a reasonable distance.")
cap.release()
