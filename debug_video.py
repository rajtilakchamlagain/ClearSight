import cv2
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine

# Master embedding
objs = DeepFace.represent('C:/Users/rajti/Downloads/messi1.jpg', model_name='ArcFace', detector_backend='mtcnn', enforce_detection=False)
master_embedding = objs[0]['embedding']

# Video frame
cap = cv2.VideoCapture('C:/Users/rajti/Downloads/messivideo.mp4')
ret, frame = cap.read()
cap.release()

if ret:
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = DeepFace.extract_faces(frame_rgb, detector_backend='mtcnn', enforce_detection=False)
    
    print(f"Found {len(faces)} faces in frame 1.")
    for i, face_obj in enumerate(faces):
        if face_obj.get('confidence', 0) == 0: continue
        facial_area = face_obj['facial_area']
        x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
        
        face_crop = frame_rgb[max(0,y):y+h, max(0,x):x+w]
        if face_crop.size == 0: continue
        
        try:
            target_objs = DeepFace.represent(img_path=face_crop, model_name='ArcFace', detector_backend='skip', enforce_detection=False)
            dist = cosine(master_embedding, target_objs[0]['embedding'])
            print(f"Face {i}: size={w}x{h}, confidence={face_obj['confidence']:.2f}, Cosine Distance={dist:.4f}")
        except Exception as e:
            print(f"Face {i}: Error computing ArcFace - {e}")
