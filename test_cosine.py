import cv2
from scipy.spatial.distance import cosine
from deepface import DeepFace

objs1 = DeepFace.represent('C:/Users/rajti/Downloads/messi1.jpg', model_name='ArcFace', detector_backend='skip', enforce_detection=False)
objs2 = DeepFace.represent('C:/Users/rajti/Downloads/messi2.jpg', model_name='ArcFace', detector_backend='skip', enforce_detection=False)

v1 = objs1[0]['embedding']
v2 = objs2[0]['embedding']

dist = cosine(v1, v2)
print(f"Cosine Distance between messi1 and messi2: {dist}")
