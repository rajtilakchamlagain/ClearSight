# 1st cell
# # 1. RIP OUT THE SLOW CPU VERSION
# !pip uninstall torch torchvision torchaudio -y

# # 2. INSTALL THE NVIDIA CUDA VERSION (High-Speed Engine)
# !pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

import torch

print("🔍 Scanning hardware for NVIDIA CUDA GPU...")

if torch.cuda.is_available():
    # Force PyTorch to use the GPU
    device = torch.device('cuda')
    gpu_name = torch.cuda.get_device_name(0)
    print(f"✅ SUCCESS: Neural Engine Locked Onto GPU: [{gpu_name}]")
    print("⚡ System is cleared for high-speed video processing!")
else:
    # If no GPU is found, crash the program immediately
    print("❌ FATAL ERROR: No GPU detected!")
    print("The system has fallen back to the extremely slow CPU. A 1-minute video will take 30+ minutes.")
    print("Aborting execution to save time.")
    raise SystemError("CUDA GPU not found! Please check your PyTorch installation or NVIDIA drivers.")

# 2nd cell
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from mtcnn import MTCNN
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
import torch.nn.functional as F

# 3rd cell
# ==========================================
# MASTER HARDWARE ROUTING
# ==========================================
print("🔍 Scanning hardware...")

# Force Python to look for the NVIDIA GPU (CUDA)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"🚀 Neural Engine Locked Onto: {device.type.upper()}")

if device.type == 'cuda':
    print(f"🔥 GPU Model: {torch.cuda.get_device_name(0)}")
    print("✅ MAXIMUM SPEED ENGAGED. Ready for real-time processing.")
else:
    print("⚠️ WARNING: Still running on CPU. Processing will be extremely slow.")

# 4th cell
import cv2
import matplotlib.pyplot as plt

# 5th cell
image_path = '../../data/test_target.jpg'

# 6th cell
# 3. READING: OpenCV reads the image and converts it into a math array
img = cv2.imread(image_path)

#7th cell
# 4. COLOR FIX: Convert from BGR (OpenCV default) to normal RGB

if img is not None:
    # 4. COLOR FIX: Convert from BGR (OpenCV default) to normal RGB
    print("Success! OpenCV found the page.")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #Display the math and the image
    print(f"The AI sees a mathematical grid of: {img_rgb.shape}")
    plt.imshow(img_rgb)
    plt.axis('off')  #(Telling the matplotlib that i don't want graph or anything,just the image)
    plt.show()
else:
    print("Error: Could not load image. Please check the file path.")

# 8th cell
image_path = '../../data/test_target2.jpg'
img = cv2.imread(image_path)
if img is not None:
    print("Success! OpenCV found the page.")
    img2_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print(f"The AI sees a mathematical grid of: {img2_rgb.shape}")
    plt.imshow(img2_rgb)
    plt.axis('off') 
    plt.show()
else:
    print("Error: Could not load image. Please check the file path.")

# 9th cell
import os

# 1. Ask Python exactly what folder it is currently inside
current_location = os.getcwd()
print(f"📍 Python is currently standing in:\n{current_location}\n")

# 2. Look at all the files/folders right next to Python
print("📁 Files and folders available right here:")
for item in os.listdir('.'):
    print(f" - {item}")

#10th cell
import os

# WHAT WE ARE DOING: Stepping back two directory levels using '../../'
# WHY: Since the kernel is trapped inside the hidden '.ipynb_checkpoints' subfolder, 
# we must step out of the checkpoint folder, then out of the notebooks folder, to hit the project root.
fail_safe_data_path = "../../data/"

print("Scanning the true project data folder...")
try:
    files = os.listdir(fail_safe_data_path)
    print("📁 Success! Found these files in your data folder:")
    for file in files:
        print(f" - {file}")
except FileNotFoundError:
    print("❌ Even stepping back twice failed. The data folder path is warped.")

# 11th cell
import os

# WHAT WE ARE DOING: Stepping back two directory levels using '../../'
# WHY: Since the kernel is trapped inside the hidden '.ipynb_checkpoints' subfolder, 
# we must step out of the checkpoint folder, then out of the notebooks folder, to hit the project root.
fail_safe_data_path = "../../data/"

print("Scanning the true project data folder...")
try:
    files = os.listdir(fail_safe_data_path)
    print("📁 Success! Found these files in your data folder:")
    for file in files:
        print(f" - {file}")
except FileNotFoundError:
    print("❌ Even stepping back twice failed. The data folder path is warped.")

# 12th cell
from mtcnn import MTCNN
from facenet_pytorch import MTCNN, InceptionResnetV1

# 13th cell
#Saving it and activating it in my computer memory
print("🧠 Waking up original MTCNN Engine...")
detector = MTCNN(thresholds=[0.7, 0.8, 0.8], device=device)  # Use the GPU if available    

# 14th cell
# Initialize GPU MTCNN
detector = MTCNN(thresholds=[0.7, 0.8, 0.8], device=device) 

# --- NEW: BACKWARDS-COMPATIBILITY WRAPPER ---
# This bridges the fast GPU engine to your old dictionary code!
def detect_faces_gpu(img_rgb):
    boxes, probs, landmarks = detector.detect(img_rgb, landmarks=True)
    faces = []
    if boxes is not None:
        for i in range(len(boxes)):
            # Convert raw coordinates [x1, y1, x2, y2] to [x, y, w, h]
            x1, y1, x2, y2 = boxes[i].astype(int)
            w, h = x2 - x1, y2 - y1
            keypoints = {
                'left_eye': landmarks[i][0].astype(int).tolist(),
                'right_eye': landmarks[i][1].astype(int).tolist()
            }
            faces.append({'box': [x1, y1, w, h], 'keypoints': keypoints})
    return faces

# 15th cell
from mtcnn import MTCNN
import cv2
import matplotlib.pyplot as plt

# 1. Force load the detector in this exact cell so it never forgets!
print("Loading MTCNN Detector...")
detector = MTCNN(steps_threshold=[0.7, 0.8, 0.8])

# 2. Copy the image so we don't permanently draw on the original data
img_with_box = img_rgb.copy()

# 3. Detect the faces
print("Scanning for faces...")
faces = detector.detect_faces(img_rgb)

# 4. Loop through every face the AI found and draw a green box around it
for face in faces:
    x, y, width, height = face['box']
    cv2.rectangle(img_with_box, (x, y), (x + width, y + height), (0, 255, 0), 5)

# 5. Display the final result
plt.imshow(img_with_box)
plt.axis('off')
plt.title("ClearSight: Targets Locked")
plt.show()

# 16th cell
# Initialize GPU MTCNN
detector = MTCNN(thresholds=[0.7, 0.8, 0.8], device=device) 

# --- NEW: BACKWARDS-COMPATIBILITY WRAPPER ---
# This bridges the fast GPU engine to your old dictionary code!
def detect_faces_gpu(img_rgb):
    boxes, probs, landmarks = detector.detect(img_rgb, landmarks=True)
    faces = []
    if boxes is not None:
        for i in range(len(boxes)):
            # Convert raw coordinates [x1, y1, x2, y2] to [x, y, w, h]
            x1, y1, x2, y2 = boxes[i].astype(int)
            w, h = x2 - x1, y2 - y1
            keypoints = {
                'left_eye': landmarks[i][0].astype(int).tolist(),
                'right_eye': landmarks[i][1].astype(int).tolist()
            }
            faces.append({'box': [x1, y1, w, h], 'keypoints': keypoints})
    return faces

# 17th cell
# Customizing the sensitivity
# Default is [0.6, 0.7, 0.7]. We are lowering it to [0.4, 0.5, 0.5] to catch side-profiles.
detector_tuned = MTCNN(steps_threshold=[0.4, 0.5, 0.5])

# 18th cell
# Let's scan it again
print("Scanning with tuned sensitivity...")
faces_tuned = detector_tuned.detect_faces(img_rgb)
print(f"Target(s) Acquired! The AI now found {len(faces_tuned)} face(s).")

# 19th cell
#Drawing the boxes and displaying it
img_tuned_box = img_rgb.copy()
for face in faces_tuned:
    x,y,width,height = face['box']
    cv2.rectangle(img_tuned_box, (x,y),(x + width , y + height) , (0,2550,0),5)

plt.imshow(img_tuned_box)
plt.axis('off')
plt.title("ClearSight: Advanced Target Lock")
plt.show()

# 20th cell
# Changed img2_rgb back to img_rgb to match our Phase 1 matrix
faces = detector.detect_faces(img_rgb)

# How many images are found
print(f"Target(s) Acquired! The AI found {len(faces)} face(s).")

# 21st cell
faces_tuned = detector_tuned.detect_faces(img2_rgb)
print(f"Target(s) Acquired! The AI now found {len(faces_tuned)} face(s).")

# 22nd cell
img2_tuned_box = img2_rgb.copy()
for face in faces_tuned:
    x,y,width,height = face['box']
    cv2.rectangle(img2_tuned_box, (x,y),(x + width ,y + height) , (0,255,0),5)

plt.imshow(img2_tuned_box)
plt.axis('off')
plt.title("ClearSight: Advanced Target Lock")
plt.show()

# 23rd cell
#Checking for another image
image_path = '../../data/test_target3.jpeg'
img = cv2.imread(image_path)
if img is not None:
    print("Success! OpenCV found the page.")
    img3_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print(f"The AI sees a mathematical grid of: {img3_rgb.shape}")
    plt.imshow(img3_rgb)
    plt.axis('off') 
    plt.show()
else:
    print("Error: Could not load image. Please check the file path.")

print("Scanning with tuned sensitivity...")
faces_tuned = detector_tuned.detect_faces(img3_rgb)
print(f"Target(s) Acquired! The AI now found {len(faces_tuned)} face(s).")

img3_tuned_box = img3_rgb.copy()
for face in faces_tuned:
    x,y,width,height = face['box']
    cv2.rectangle(img3_tuned_box, (x,y),(x + width , y + height) , (0,255,0),5)

plt.imshow(img3_tuned_box)
plt.axis('off')
plt.title("ClearSight: Advanced Target Lock")
plt.show()

# 24th cell
#1. Creating a array to store our isolated face matrices
cropped_faces = []

# 25th cell
#We will loop through the co-ordinates (found in Phase 2)
#'enumerate' is something that gives us an index counter (i) starting at 0 for naing traking
for i, face in enumerate(faces_tuned):
    x,y,width,height = face['box']

    #Applying NumPy Matrix Slicing: [y_start : y_end, x_start : x_end]
    #Cancelling the negative coordinates by customizing the range that sometimes happens near borders
    y_start = max(0, y)
    x_start = max(0, x)

    face_crop = img3_rgb[y_start : y_start + height, x_start : x_start + width]

    cropped_faces.append(face_crop) #(Now the matrix will be stored in memory)

    #Now we have to check each faces independentely to verify the mathmetical cuts
    plt.figure(figsize=(2,2))  #(Keeps the displayed target sizes small and clean)
    plt.imshow(face_crop)
    plt.axis('off')
    plt.title(f"Target Matrix {i+1}")
    plt.show()

# 26th cell
image_path = '../../data/test_target4.jpeg'
img = cv2.imread(image_path)
if img is not None:
    print("Success! OpenCV found the page.")
    img4_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print(f"The AI sees a mathematical grid of: {img4_rgb.shape}")
    plt.imshow(img4_rgb)
    plt.axis('off') 
    plt.show()
else:
    print("Error: Could not load image. Please check the file path.")

print("Scanning with tuned sensitivity...")
faces_tuned = detector_tuned.detect_faces(img4_rgb)
print(f"Target(s) Acquired! The AI now found {len(faces_tuned)} face(s).")

img4_tuned_box = img4_rgb.copy()
for face in faces_tuned:
    x,y,width,height = face['box']
    cv2.rectangle(img4_tuned_box, (x,y),(x + width , y + height) , (0,255,0),5)

plt.imshow(img4_tuned_box)
plt.axis('off')
plt.title("ClearSight: Advanced Target Lock")
plt.show()

# 27th cell
for i, face in enumerate(faces_tuned):
    x,y,width,height = face['box']

    #Applying NumPy Matrix Slicing: [y_start : y_end, x_start : x_end]
    #Cancelling the negative coordinates by customizing the range that sometimes happens near borders
    y_start = max(0, y)
    x_start = max(0, x)

    face_crop = img4_rgb[y_start : y_start + height, x_start : x_start + width]

    cropped_faces.append(face_crop) #(Now the matrix will be stored in memory)

    #Now we have to check each faces independentely to verify the mathmetical cuts
    plt.figure(figsize=(2,2))  #(Keeps the displayed target sizes small and clean)
    plt.imshow(face_crop)
    plt.axis('off')
    plt.title(f"Target Matrix {i+1}")
    plt.show()

# 28th cell
import os
import cv2

# 29th cell
#Creating new folder inside data folder to save the photos(The above photos are temporarily stored in RAM but we will be needing actual stored images for later)
save_folder = '../../data/extracted_faces'
os.makedirs(save_folder, exist_ok=True) # exist_ok = True prevents crashes if the folder is already there)

#Loop through the matrices for storing the images/matrix
for i, face_matrix in enumerate(cropped_faces):
    face_bgr = cv2.cvtColor(face_matrix, cv2.COLOR_RGB2BGR) #(Flips the colors back from RGB to BGR)
    file_path = f"{save_folder}/target_{i+1}.jpg" #(It will generate a unique file name(e.g.,target_1.jpg)
    cv2.imwrite(file_path, face_bgr) #(Physically write the file in the memory
print(f"Success! {len(cropped_faces)} targets have been permenently saved to:{save_folder}")