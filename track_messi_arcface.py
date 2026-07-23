import cv2
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine

# 1. Configuration
MASTER_IMAGE = 'C:/Users/rajti/Downloads/messi1.jpg'
VIDEO_INPUT = 'C:/Users/rajti/Downloads/messivideo.mp4'
VIDEO_OUTPUT = 'C:/Users/rajti/Downloads/messivideo_tracked.mp4'
THRESHOLD = 0.68  # ArcFace Cosine Threshold

print("Step 1: Generating Master Vector for Messi...")
try:
    master_objs = DeepFace.represent(img_path=MASTER_IMAGE, model_name='ArcFace', detector_backend='yolov8')
    master_vector = master_objs[0]['embedding']
    print(f"Master Vector Locked. Dimension: {len(master_vector)}")
except Exception as e:
    print(f"Error loading master image: {e}")
    exit()

# 2. Open Video
cap = cv2.VideoCapture(VIDEO_INPUT)
if not cap.isOpened():
    print(f"Error: Could not open video {VIDEO_INPUT}")
    exit()

# Get video properties for saving
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(VIDEO_OUTPUT, fourcc, fps, (width, height))

print(f"Step 2: Scanning Video ({total_frames} frames)...")

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    # To speed up processing, process every 2nd frame, or process all. Let's process all for max accuracy.
    print(f"Processing Frame {frame_count}/{total_frames}...")

    # OpenCV loads in BGR. DeepFace expects BGR for numpy arrays, but we convert to RGB for safety just in case.
    # Actually DeepFace handles BGR numpy arrays perfectly.
    
    try:
        # Step 2A: Detect all faces in the frame using RetinaFace
        # We set enforce_detection=False so it doesn't crash if a frame has no faces
        faces = DeepFace.extract_faces(img_path=frame, detector_backend='yolov8', enforce_detection=False)
        
        for face_obj in faces:
            # If no face is found, DeepFace sometimes returns a dummy dict with confidence 0
            if face_obj.get('confidence', 0) == 0:
                continue
                
            facial_area = face_obj['facial_area']
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            
            # Crop the face safely
            y1, y2 = max(0, y), min(height, y + h)
            x1, x2 = max(0, x), min(width, x + w)
            face_crop = frame[y1:y2, x1:x2]
            
            if face_crop.size == 0:
                continue

            # Step 2B: Generate ArcFace mathematical vector for this face
            # We use detector_backend='skip' because it's already cropped!
            target_objs = DeepFace.represent(img_path=face_crop, model_name='ArcFace', detector_backend='skip', enforce_detection=False)
            target_vector = target_objs[0]['embedding']
            
            # Step 2C: Calculate Cosine Distance
            distance = cosine(master_vector, target_vector)
            
            # Step 2D: Draw Bounding Box
            if distance < THRESHOLD:
                # MATCH FOUND! (Green Box)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, f"TARGET LOCKED [{distance:.2f}]", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # STRANGER (Red Box)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, f"UNKNOWN [{distance:.2f}]", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
    except Exception as e:
        # If RetinaFace fails on a blurry frame, just ignore and continue
        pass

    # Save the frame
    out.write(frame)

cap.release()
out.release()
print(f"Tracking Complete! Video saved to {VIDEO_OUTPUT}")
