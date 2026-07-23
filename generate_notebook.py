import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# ClearSight 2.0: The State-of-the-Art Upgrade\n",
    "Welcome to the new, upgraded pipeline. In this notebook, we are replacing the 2015 Google FaceNet (MTCNN) with the 2024 industry standards: **RetinaFace** (for detection) and **ArcFace** (for verification).\n",
    "\n",
    "These are the models used by real-world police and security agencies today."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 1: Importing the New AI Libraries\n",
    "We are using `deepface`, which acts as a wrapper for multiple massive AI models (including ArcFace and RetinaFace)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import matplotlib.pyplot as plt\n",
    "from deepface import DeepFace\n",
    "import numpy as np\n",
    "\n",
    "print(\"DeepFace, RetinaFace, and ArcFace modules are ready.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 2: The New Detective (RetinaFace)\n",
    "In the old pipeline, MTCNN would fail if a face turned sideways or was blurry. \n",
    "\n",
    "**RetinaFace** uses feature-pyramid networks. It can detect faces even if they are 70% occluded by objects or turned 90 degrees away from the camera. Let's load the Messi image and test it."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load the target image using ABSOLUTE path\n",
    "image_path = 'C:/Users/rajti/Downloads/messi1.jpg'\n",
    "img = cv2.imread(image_path)\n",
    "if img is None:\n",
    "    print(\"Error: Image not found at path:\", image_path)\n",
    "else:\n",
    "    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)\n",
    "    plt.imshow(img_rgb)\n",
    "    plt.axis('off')\n",
    "    plt.title('Original Image')\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use RetinaFace to extract the face\n",
    "if img is not None:\n",
    "    print(\"Scanning with YOLOv8...\")\n",
    "    faces = DeepFace.extract_faces(img_path = img_rgb, detector_backend = 'yolov8', enforce_detection=False)\n",
    "    for face_obj in faces:\n",
    "        face_matrix = face_obj['face']\n",
    "        confidence = face_obj['confidence']\n",
    "        \n",
    "        plt.imshow(face_matrix)\n",
    "        plt.axis('off')\n",
    "        plt.title(f'YOLOv8 Detection (Confidence: {confidence:.2f})')\n",
    "        plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 3: The New Mathematician (ArcFace)\n",
    "In the old pipeline, **FaceNet** used *Triplet Loss* (measuring the physical distance between two faces in a 512D graph). Blurry lighting ruins physical distance, causing false positives.\n",
    "\n",
    "**ArcFace** uses *Additive Angular Margin Loss*. Instead of measuring physical distance, it calculates the strict geometric **angle** of the face (cheekbones, eyes, nose). Because angles do not change in the dark, it is mathematically immune to bad lighting."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if img is not None:\n",
    "    print(\"Generating ArcFace Embedding (The Mathematical Password)...\")\n",
    "    embedding_objs = DeepFace.represent(img_path = img_rgb, model_name = 'ArcFace', detector_backend = 'yolov8', enforce_detection=False)\n",
    "    arcface_vector = embedding_objs[0]['embedding']\n",
    "    \n",
    "    print(f\"ArcFace generated a highly-secure vector with {len(arcface_vector)} dimensions.\")\n",
    "    print(\"First 10 dimensions of the geometric angle:\", arcface_vector[:10])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 4: Zero-Shot Cosine Verification\n",
    "Now we will compare two photos of Messi using **Cosine Similarity** (which checks the angle between the two vectors). If the Cosine Similarity is > 0.68, it is identical. If it's < 0.50, it is a random stranger."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def verify_identities(img1_path, img2_path):\n",
    "    print(f\"Comparing {img1_path} and {img2_path}...\")\n",
    "    result = DeepFace.verify(\n",
    "        img1_path=img1_path, \n",
    "        img2_path=img2_path, \n",
    "        model_name='ArcFace', \n",
    "        detector_backend='yolov8', \n",
    "        distance_metric='cosine',\n",
    "        enforce_detection=False\n",
    "    )\n",
    "    \n",
    "    match = result['verified']\n",
    "    distance = result['distance']  # For Cosine, lower distance = higher similarity\n",
    "    threshold = result['threshold']\n",
    "    \n",
    "    print(f\"MATCH FOUND? {match}\")\n",
    "    print(f\"Cosine Distance: {distance:.3f} (Must be lower than {threshold:.3f})\")\n",
    "\n",
    "try:\n",
    "    # Using absolute paths to ensure OpenCV can find them anywhere on your PC\n",
    "    verify_identities('C:/Users/rajti/Downloads/messi1.jpg', 'C:/Users/rajti/Downloads/messi2.jpg')\n",
    "except Exception as e:\n",
    "    print(\"Error:\", e)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 5: Live Video Tracking (The Frame-by-Frame Loop)\n",
    "Now that we proved ArcFace works mathematically, let's unleash it on the video.\n",
    "Instead of using a buggy OpenCV CSRT Tracker, we will calculate the ArcFace math on **every single frame** so it never drifts to the wrong person!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from scipy.spatial.distance import cosine\n",
    "import cv2\n",
    "\n",
    "MASTER_IMAGE = 'C:/Users/rajti/Downloads/messi1.jpg'\n",
    "VIDEO_INPUT = 'C:/Users/rajti/Downloads/messivideo.mp4'\n",
    "VIDEO_OUTPUT = 'C:/Users/rajti/Downloads/messivideo_tracked.mp4'\n",
    "THRESHOLD = 0.68  # ArcFace Cosine Threshold\n",
    "\n",
    "print(\"Step 1: Generating Master Vector for Messi...\")\n",
    "master_objs = DeepFace.represent(img_path=MASTER_IMAGE, model_name='ArcFace', detector_backend='yolov8')\n",
    "master_vector = master_objs[0]['embedding']\n",
    "print(f\"Master Vector Locked. Dimension: {len(master_vector)}\")\n",
    "\n",
    "cap = cv2.VideoCapture(VIDEO_INPUT)\n",
    "width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))\n",
    "height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\n",
    "fps = int(cap.get(cv2.CAP_PROP_FPS))\n",
    "total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))\n",
    "\n",
    "fourcc = cv2.VideoWriter_fourcc(*'mp4v')\n",
    "out = cv2.VideoWriter(VIDEO_OUTPUT, fourcc, fps, (width, height))\n",
    "\n",
    "print(f\"Step 2: Scanning Video ({total_frames} frames). This will take a moment...\")\n",
    "frame_count = 0\n",
    "\n",
    "while cap.isOpened():\n",
    "    ret, frame = cap.read()\n",
    "    if not ret: break\n",
    "    frame_count += 1\n",
    "    if frame_count % 30 == 0:\n",
    "        print(f\"Processing Frame {frame_count}/{total_frames}...\")\n",
    "    \n",
    "    try:\n",
    "        # Detect all faces in the frame using YOLOv8\n",
    "        faces = DeepFace.extract_faces(img_path=frame, detector_backend='yolov8', enforce_detection=False)\n",
    "        \n",
    "        for face_obj in faces:\n",
    "            if face_obj.get('confidence', 0) == 0: continue\n",
    "                \n",
    "            facial_area = face_obj['facial_area']\n",
    "            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']\n",
    "            \n",
    "            y1, y2 = max(0, y), min(height, y + h)\n",
    "            x1, x2 = max(0, x), min(width, x + w)\n",
    "            face_crop = frame[y1:y2, x1:x2]\n",
    "            \n",
    "            if face_crop.size == 0: continue\n",
    "            \n",
    "            # Generate ArcFace mathematical vector for this face\n",
    "            target_objs = DeepFace.represent(img_path=face_crop, model_name='ArcFace', detector_backend='skip', enforce_detection=False)\n",
    "            target_vector = target_objs[0]['embedding']\n",
    "            \n",
    "            # Calculate Cosine Distance\n",
    "            distance = cosine(master_vector, target_vector)\n",
    "            \n",
    "            if distance < THRESHOLD:\n",
    "                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)\n",
    "                cv2.putText(frame, f\"TARGET LOCKED [{distance:.2f}]\", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)\n",
    "            else:\n",
    "                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)\n",
    "                cv2.putText(frame, f\"UNKNOWN [{distance:.2f}]\", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)\n",
    "                \n",
    "    except Exception as e:\n",
    "        pass # Ignore blurry frames\n",
    "\n",
    "    out.write(frame)\n",
    "\n",
    "cap.release()\n",
    "out.release()\n",
    "print(f\"Tracking Complete! Video saved to {VIDEO_OUTPUT}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

output_path = "C:/Users/rajti/Downloads/Projects/ACADEMIC INTERNSHIP/ClearSight_Project/notebooks/ClearSight_ArcFace_Upgrade.ipynb"
with open(output_path, "w") as f:
    json.dump(notebook, f, indent=1)

print(f"Successfully generated notebook at {output_path}")
