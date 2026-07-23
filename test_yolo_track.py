import cv2
from ultralytics import YOLO

# Load the official YOLOv8 nano model for PERSON detection (not face)
model = YOLO('yolov8n.pt')

# Run tracking on the video
results = model.track(source='C:/Users/rajti/Downloads/messivideo.mp4', classes=[0], stream=True, verbose=False)

print("Tracking video...")
frame_count = 0
for r in results:
    frame_count += 1
    if r.boxes.id is not None:
        ids = r.boxes.id.cpu().numpy().astype(int)
        print(f"Frame {frame_count}: Tracked Person IDs: {ids}")
    else:
        print(f"Frame {frame_count}: No persons tracked.")
        
    if frame_count > 5:
        break
print("Done.")
