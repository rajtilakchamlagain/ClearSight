import cv2
import torch
import numpy as np
from torchvision import transforms
import torch.nn.functional as F
import facenet_pytorch
from PIL import Image

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
detector = facenet_pytorch.MTCNN(thresholds=[0.6, 0.7, 0.7], keep_all=True, device=device)
resnet = facenet_pytorch.InceptionResnetV1(pretrained='vggface2').eval().to(device)
preprocess = transforms.Compose([
    transforms.ToPILImage(), transforms.Resize((160, 160)),
    transforms.ToTensor(), transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

def get_perfect_face(img_rgb, box):
    x1, y1, x2, y2 = box.astype(int)
    w, h = x2 - x1, y2 - y1
    x, y = max(0, x1), max(0, y1)
    face_crop = img_rgb[y:y+h, x:x+w]
    if face_crop.size == 0: return None
    lab = cv2.cvtColor(face_crop, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    cl = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    return cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2RGB)

print("Loading Master Vector...")
img = Image.open('C:/Users/rajti/Downloads/messi1.jpg').convert('RGB')
img_rgb = np.array(img)
boxes, probs = detector.detect(img_rgb)
if boxes is not None and len(boxes) > 0:
    biggest_box = max(boxes, key=lambda b: (b[2]-b[0]) * (b[3]-b[1]))
    perfect_face = get_perfect_face(img_rgb, biggest_box)
    tensor = preprocess(perfect_face).unsqueeze(0).to(device)
    with torch.no_grad():
        master_embedding = resnet(tensor)
    print("Master Vector ready.")
else:
    print("FAILED to find face in messi1.jpg")
    exit()

cap = cv2.VideoCapture('C:/Users/rajti/Downloads/messivideo.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Video loaded. {total_frames} frames. Sampling 5 frames...")

frames_to_check = [0, total_frames//4, total_frames//2, 3*total_frames//4, total_frames-2]

for f_idx in frames_to_check:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
    ret, frame = cap.read()
    if not ret: continue
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, probs = detector.detect(frame_rgb)
    
    print(f"\n--- Frame {f_idx} ---")
    if boxes is None:
        print("No faces detected in frame.")
        continue
        
    print(f"Found {len(boxes)} faces.")
    for i, box in enumerate(boxes):
        w, h = box[2]-box[0], box[3]-box[1]
        perfect_face = get_perfect_face(frame_rgb, box)
        if perfect_face is None: continue
        
        with torch.no_grad():
            tensor = preprocess(perfect_face).unsqueeze(0).to(device)
            embedding = resnet(tensor)
            
        sim = F.cosine_similarity(master_embedding, embedding).item()
        print(f"Face {i+1}: Size {int(w)}x{int(h)}, Confidence {probs[i]:.2f}, Similarity to Messi: {sim:.4f}")

cap.release()
print("Done.")
