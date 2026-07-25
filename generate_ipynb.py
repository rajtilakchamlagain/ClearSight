import nbformat as nbf

with open('test_all.py', encoding='utf-8') as f:
    code = f.read()

nb = nbf.v4.new_notebook()

markdown_header = """# ClearSight AI: Industrial-Grade Target Person Search & ReID Engine
**Developer:** Raj Tilak Chamlagain (RTC Core Developer)  
**Project Type:** Academic Internship under Dr. Mahapara K.

---
### 💠 Enterprise Multi-Modal Architecture
This notebook implements an industrial **Person Re-Identification (ReID) in the Wild** and **Image-to-Video Target Search** system designed to overcome complex surveillance challenges such as identical sports jerseys, severe occlusion, and dark lighting.

#### Core Technological Innovations:
1. **Biometric Face Vector Gallery:** Employs **InsightFace ArcFace (ResNet-50)** to capture high-resolution deep biometric signatures whenever a target's face is discernible.
2. **Whole-Body Semantic Feature Extraction:** Integrates **PyTorch MobileNetV3** trained on general computer vision datasets to capture posture, proportions, and deep structural visual features.
3. **HSV Apparel Spatial Signatures:** Uses 2D spatial color histograms divided into upper and lower garment ratios for lighting-invariant apparel tracking.
4. **Forensic Biometric Veto Rule:** Eliminates identity bleeding in complex scenes (such as soccer matches where all teammates wear identically colored uniforms). If a tracklet captures a clear facial image that contradicts the Master Reference photo, the system **instantly vetoes and silently discards** that subject.
5. **Adaptive Confidence Thresholding & Backend Pruning:** Calculates personalized similarity thresholds dynamically relative to primary target anchors while eliminating flickering boxes and noisy background detections from user output.
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(markdown_header),
    nbf.v4.new_code_cell("# Run Automated Verification Benchmark across Movie Scenes & Sports Footage\n" + code)
]

nbf.write(nb, 'ClearSight_Face_Tracking.ipynb')
nbf.write(nb, 'ClearSight_Industrial_ReID.ipynb')
print("[SUCCESS] Successfully created ClearSight_Face_Tracking.ipynb and ClearSight_Industrial_ReID.ipynb!")
