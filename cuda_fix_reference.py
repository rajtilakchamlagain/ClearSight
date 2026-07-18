import os
import cv2
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
from mtcnn import MTCNN

# -----------------------------
# CUDA ROUTING (FIXED)
# -----------------------------
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device selected: {device}")

if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
else:
    print("GPU not detected. Running on CPU.")

# -----------------------------
# MODEL + PREPROCESSING
# -----------------------------
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

# -----------------------------
# IMAGE LOAD
# -----------------------------
image_path = os.path.join('data', 'test_target3.jpeg')
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"Could not open: {image_path}")

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# -----------------------------
# FACE DETECTION
# -----------------------------
detector = MTCNN(steps_threshold=[0.4, 0.5, 0.5])
faces = detector.detect_faces(img_rgb)
print(f"Faces found: {len(faces)}")

cropped_faces = []
for face in faces:
    x, y, width, height = face['box']
    x_start = max(0, x)
    y_start = max(0, y)
    face_crop = img_rgb[y_start:y_start + height, x_start:x_start + width]
    cropped_faces.append(face_crop)

# -----------------------------
# KNOWN FACE
# -----------------------------
known_path = os.path.join('data', 'rajtilak_face.jpeg')
known_img_cv = cv2.imread(known_path)
if known_img_cv is None:
    raise FileNotFoundError(f"Could not open known face: {known_path}")
known_img_rgb = cv2.cvtColor(known_img_cv, cv2.COLOR_BGR2RGB)

# -----------------------------
# GPU SAFE EMBEDDING EXTRACTION
# -----------------------------
known_tensor = preprocess(known_img_rgb).unsqueeze(0).to(device)
with torch.no_grad():
    known_embedding = resnet(known_tensor).cpu()

MATCH_THRESHOLD = 0.60
confirmed = 0

for i, face_matrix in enumerate(cropped_faces):
    unknown_tensor = preprocess(face_matrix).unsqueeze(0).to(device)
    with torch.no_grad():
        unknown_embedding = resnet(unknown_tensor).cpu()

    similarity = F.cosine_similarity(known_embedding, unknown_embedding).item()
    is_match = similarity > MATCH_THRESHOLD

    print(f"Target {i + 1}: similarity = {similarity:.4f} -> {'MATCH' if is_match else 'NO MATCH'}")

    if is_match:
        confirmed += 1

print(f"Confirmed targets: {confirmed}")
