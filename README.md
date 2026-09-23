# ClearSight AI: Forensic Person Re-Identification

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clearsight-ai.streamlit.app)

An advanced Video Person Re-Identification (Re-ID) tracking pipeline engineered to eliminate "Threshold Guessing" in blurry or low-light CCTV footage. Built during an academic internship at the Technology Innovation Hub (TIH-TIDF), IIT Guwahati.

## 🚀 Live Demo & Local Execution

**Live Web App:** [https://clearsight-ai.streamlit.app](https://clearsight-ai.streamlit.app) *(Requires Streamlit Cloud deployment)*

**Run Locally:**
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the application: `streamlit run app.py` (or `python start.py` on Windows to avoid SSL errors)
4. The dashboard will be available at: **http://localhost:8501**

## 🧠 Core Innovations
- **Autonomous Spectral Gap Engine**: Dynamically calculates the maximal first-derivative drop-off between facial similarity vectors to autonomously place a zero-shot threshold gate. Completely removes human bias from evidence triage.
- **Kinetic Occlusion Recovery**: Utilizes ByteTrack's Kalman Filters to mathematically predict subject trajectories, allowing tracking to survive massive crowd occlusions even when the subject's face is completely hidden.
- **Native Disk Sockets**: Bypasses traditional HTML DOM Base64 memory bloat by streaming massive video binary data directly via sockets, ensuring the dashboard runs smoothly on lower-end forensic hardware without crashing.

## 🛠️ Tech Stack
- **Deep Learning Architecture**: PyTorch, YOLOv8 (Kinetic Detection), ArcFace 512D (Biometric Encoding), RetinaFace (Affine Landmark Alignment)
- **Algorithmic Math**: NumPy (Cosine Similarity & Derivative Threshold Analysis)
- **Frontend Dashboard**: Streamlit 

> **Note on Cloud Deployment:** Running YOLOv8, ArcFace, and MobileNetV3 concurrently requires ~800MB - 1.2GB of RAM. If deploying on Streamlit Cloud's free tier (1GB limit), you may encounter Out-Of-Memory (OOM) errors during heavy video processing.

*Engineered by Rajtilak Chamlagain under the supervision of Dr. Mahapara Khursid (IIT Guwahati).*

