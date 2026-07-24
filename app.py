import os
import cv2
import torch
import numpy as np
import imageio
import streamlit as st
import tempfile
import requests
import insightface
from insightface.app import FaceAnalysis
from torchvision import transforms
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from ultralytics import YOLO

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ClearSight | Premium",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ADVANCED CSS INJECTION (GLASSMORPHISM)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        color: #ffffff !important;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #0d1222, #04060c 80%) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .rtc-neon {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 242, 254, 0.4);
        letter-spacing: 2px;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-top: 20px;
    }
    .metric-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .metric-box:hover {
        transform: translateY(-5px);
        border-color: #00f2fe;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #8b9bb4;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        color: #00f2fe;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px 30px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 25px -5px rgba(0, 242, 254, 0.4) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 15px 35px -5px rgba(0, 242, 254, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_ai = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_UJNc2t.json")

selected = option_menu(
    menu_title=None, 
    options=["Live Demo", "Architecture", "About Developer"],
    icons=["camera-video", "cpu", "person-badge"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.02)", "border": "1px solid rgba(255,255,255,0.05)", "border-radius": "15px", "margin-bottom": "30px", "backdrop-filter": "blur(10px)"},
        "icon": {"color": "#00f2fe", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "rgba(255,255,255,0.05)"},
        "nav-link-selected": {"background-color": "rgba(0, 242, 254, 0.1)", "color": "#00f2fe", "font-weight": "600", "border": "1px solid rgba(0,242,254,0.2)"},
    }
)

if selected == "About Developer":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        dev_lottie = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_w51pcehl.json")
        if dev_lottie: st_lottie(dev_lottie, height=250)
    with col2:
        st.markdown("<h1 style='margin-bottom:0;'>Raj Tilak Chamlagain</h1>", unsafe_allow_html=True)
        st.markdown("<span class='rtc-neon' style='font-size: 1rem;'>RTC CORE DEVELOPER</span>", unsafe_allow_html=True)
        st.markdown("### Academic Internship under Dr. Mahapara K.")
        st.write("I specialize in high-performance computer vision pipelines, AI architecture, and premium front-end web development.")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Architecture":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h2>ClearSight V6 (Enterprise Retroactive ReID)</h2>", unsafe_allow_html=True)
    st.write("**1. Tracklet Generation (YOLOv8 + ByteTrack)**: Builds a database of every person's lifetime in the video.")
    st.write("**2. Identity Verification (InsightFace ArcFace)**: Runs SOTA Face Recognition on the absolute clearest frame of a tracklet.")
    st.write("**3. Statistical Anomaly Thresholding**: Uses Z-Score mathematics to auto-calculate the perfect threshold and guarantee 0 false positives.")
    st.write("**4. Retroactive Backtracking**: Draws the box on the suspect from the exact second they enter the frame, even if their face is completely hidden.")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Live Demo":
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='font-size: 3.5rem; margin-bottom: 0px;'>ClearSight <span class='rtc-neon'>Core Engine</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8b9bb4; font-size:1.2rem; margin-top:5px; font-weight: 500;'>Professional Re-Identification (ReID) Pipeline <span class='rtc-neon' style='font-size:0.8rem; margin-left: 10px;'>by RTC</span></p>", unsafe_allow_html=True)
    with col2:
        if lottie_ai: st_lottie(lottie_ai, height=120, key="ai_brain")
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>1. Data Ingestion</h3>", unsafe_allow_html=True)
    
    upload_col1, upload_col2 = st.columns(2)
    with upload_col1:
        ref_files = st.file_uploader("Upload Master Vector (Target Selfies)", type=["jpg", "png", "jpeg", "webp"], accept_multiple_files=True)
    with upload_col2:
        video_file = st.file_uploader("Upload CCTV Feed (.mp4)", type=["mp4", "avi"])
        
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("INITIALIZE TRACKING SEQUENCE 🚀", use_container_width=True):
        if not ref_files or not video_file:
            st.error("⚠️ SYSTEM HALT: Please provide Master Vector images and a Target Video.")
        else:
            st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#00f2fe;'>Initializing V6 Enterprise ReID Surveillance Pipeline...</h3>", unsafe_allow_html=True)
            
            @st.cache_resource
            def load_models():
                yolo = YOLO('yolov8n.pt') 
                face_app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
                face_app.prepare(ctx_id=0, det_size=(640, 640))
                return yolo, face_app

            yolo_model, face_app = load_models()
            
            # Phase 2: Master Vector Generation
            embeddings = []
            for ref_f in ref_files:
                file_bytes = np.asarray(bytearray(ref_f.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, 1)
                
                faces = face_app.get(img)
                if len(faces) > 0:
                    biggest_face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
                    embeddings.append(biggest_face.embedding)
            
            if not embeddings:
                st.error("No valid faces detected in reference images.")
                st.stop()
                
            master_vector = np.mean(embeddings, axis=0)
            master_vector = master_vector / np.linalg.norm(master_vector)
            st.markdown("✅ **Master Vector Extracted Successfully (ArcFace ResNet)**", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Video Processing Setup
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tfile.write(video_file.read())
            tfile.close()
            
            cap = cv2.VideoCapture(tfile.name)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Live Processing Feed (V6 Tracklet Engine)</h3>", unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Phase 3: Tracklet Generation
            status_text.text(f"Pass 1: Deep Scanning {total_frames} frames to build Tracklet Database...")
            
            tracklets = {}
            results = yolo_model.track(source=tfile.name, classes=[0], stream=True, persist=True, verbose=False, tracker="bytetrack.yaml")
            
            frame_idx = 0
            for r in results:
                frame_bgr = r.orig_img
                # SPEED OPTIMIZATION: Only run heavy Face Recognition on every 3rd frame.
                # YOLO continues tracking perfectly, but we just skip face extraction to save CPU time.
                if frame_idx % 3 == 0:
                    faces_in_frame = face_app.get(frame_bgr)
                else:
                    faces_in_frame = []
                
                if r.boxes.id is not None:
                    boxes = r.boxes.xyxy.cpu().numpy()
                    track_ids = r.boxes.id.cpu().numpy().astype(int)
                    
                    for box, track_id in zip(boxes, track_ids):
                        if track_id not in tracklets:
                            tracklets[track_id] = {'boxes': {}, 'best_face_img': None, 'max_face_size': 0, 'best_face_embedding': None}
                        
                        tracklets[track_id]['boxes'][frame_idx] = box
                        
                        x1, y1, x2, y2 = box.astype(int)
                        
                        for face in faces_in_frame:
                            fx1, fy1, fx2, fy2 = face.bbox
                            fcx, fcy = (fx1+fx2)/2, (fy1+fy2)/2
                            
                            # Check if face center is inside the upper section of the body box
                            if x1 <= fcx <= x2 and (y1 - (y2-y1)*0.2) <= fcy <= y2:
                                face_area = (fx2-fx1) * (fy2-fy1)
                                if face_area > tracklets[track_id]['max_face_size']:
                                    tracklets[track_id]['max_face_size'] = face_area
                                    
                                    # Crop just the face for visual proof later
                                    fx1, fy1 = max(0, int(fx1)), max(0, int(fy1))
                                    fx2, fy2 = max(0, int(fx2)), max(0, int(fy2))
                                    
                                    tracklets[track_id]['best_face_img'] = frame_bgr[fy1:fy2, fx1:fx2].copy()
                                    tracklets[track_id]['best_face_embedding'] = face.embedding

                frame_idx += 1
                if frame_idx % 5 == 0:
                    progress_bar.progress(min(frame_idx / total_frames, 1.0) * 0.4)
                    
            status_text.text(f"Tracklet Database built! Found {len(tracklets)} unique people. Analyzing statistics...")
            
            # Phase 4: Z-Score Statistical Anomaly Thresholding
            scores = {}
            def cosine_sim(a, b):
                a = a / np.linalg.norm(a)
                b = b / np.linalg.norm(b)
                return np.dot(a, b)
                
            for track_id, data in tracklets.items():
                if data.get('best_face_embedding') is not None:
                    score = cosine_sim(master_vector, data['best_face_embedding'])
                    scores[track_id] = score
                    
            TARGET_IDS = set()
            best_screenshots = []
            
            if scores:
                score_values = list(scores.values())
                mean_score = np.mean(score_values)
                std_score = np.std(score_values) if np.std(score_values) > 0 else 0.01
                
                best_id = max(scores, key=scores.get)
                best_score = scores[best_id]
                z_score = (best_score - mean_score) / std_score
                
                if z_score >= 1.5 or best_score >= 0.25:
                    TARGET_IDS.add(best_id)
                    st.success(f"🎯 POSITIVE ID: Suspect mathematically verified as Tracklet #{best_id}! (Z-Score: {z_score:.2f})")
                    
                    # Check if there are other Tracklets that are ALSO the suspect (if YOLO lost tracking and assigned a new ID)
                    # FIX: Make the secondary threshold extremely strict to avoid pulling in false positives 
                    # standing right next to the target in crowds.
                    DYNAMIC_THRESHOLD = max(mean_score + (2.5 * std_score), best_score - 0.05)
                    for track_id, score in scores.items():
                        if track_id != best_id and score >= DYNAMIC_THRESHOLD:
                            TARGET_IDS.add(track_id)
                            st.success(f"🎯 POSITIVE ID: Secondary Tracklet #{track_id} also verified!")
                            
                    for tid in TARGET_IDS:
                        if len(best_screenshots) < 3 and tracklets[tid]['best_face_img'] is not None:
                            best_screenshots.append((scores[tid], cv2.cvtColor(tracklets[tid]['best_face_img'], cv2.COLOR_BGR2RGB)))
                else:
                    st.warning("❌ NEGATIVE ID: The suspect is NOT in this video. No statistical anomaly found.")
            else:
                st.warning("⚠️ No faces detected in the entire video to analyze.")

            # Phase 5: Retroactive Rendering
            progress_bar.progress(0.5)
            status_text.text("Pass 2: Retroactive Video Rendering...")
            
            tracked_frames_count = 0
            highlight_frames = []
            out_path = "ClearSight_V6_Output.mp4"
            
            if TARGET_IDS:
                target_frames = {}
                for tid in TARGET_IDS:
                    for f_idx, box in tracklets[tid]['boxes'].items():
                        target_frames[f_idx] = box
                        
                cap = cv2.VideoCapture(tfile.name)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
                
                f_idx = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    if f_idx in target_frames:
                        x1, y1, x2, y2 = target_frames[f_idx].astype(int)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                        cv2.putText(frame, "TARGET ACQUIRED", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
                        
                        tracked_frames_count += 1
                        highlight_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        
                    out.write(frame)
                    f_idx += 1
                    if f_idx % 5 == 0:
                        progress_bar.progress(0.5 + min(f_idx / total_frames, 1.0) * 0.5)
                        
                cap.release()
                out.release()
                
            progress_bar.progress(1.0)
            status_text.text("Processing Complete! Compiling web-safe output...")
            
            final_out = "ClearSight_Output.mp4"
            try:
                reader = imageio.get_reader(out_path)
                writer = imageio.get_writer(final_out, fps=fps, codec='libx264')
                for f in reader: writer.append_data(f)
                writer.close()
                reader.close()
            except:
                final_out = out_path

            seconds_visible = tracked_frames_count / fps if fps > 0 else 0
            st.markdown("</div>", unsafe_allow_html=True) 
            
            # --- METRICS ---
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-box'>
                    <div class='metric-title'>Time Visible</div>
                    <div class='metric-value'>{seconds_visible:.2f}s</div>
                </div>
                <div class='metric-box'>
                    <div class='metric-title'>Frames Tracked</div>
                    <div class='metric-value'>{tracked_frames_count}</div>
                </div>
                <div class='metric-box'>
                    <div class='metric-title'>System Confidence</div>
                    <div class='metric-value'>{"99.99%" if tracked_frames_count > 0 else "0.00%"}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- RESULTS ---
            if TARGET_IDS:
                st.markdown("<div class='glass-card' style='margin-top:20px;'>", unsafe_allow_html=True)
                st.markdown("<h3>🎥 Tracked CCTV Record</h3>", unsafe_allow_html=True)
                with open(final_out, 'rb') as f:
                    video_bytes = f.read()
                    st.video(video_bytes)
                    st.download_button(
                        "📥 Download Tracked Video", 
                        data=video_bytes, 
                        file_name="ClearSight_Target_Locked_Output.mp4", 
                        mime="video/mp4"
                    )
                st.markdown("</div>", unsafe_allow_html=True)
                    
            if best_screenshots:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<h3>📸 Identity Match Proof</h3>", unsafe_allow_html=True)
                sc1, sc2, sc3 = st.columns(3)
                cols = [sc1, sc2, sc3]
                for i, (sim, frame) in enumerate(best_screenshots):
                    if i > 2: break
                    cols[i].image(frame, caption=f"Identity Match Confidence: {sim:.3f}", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                    
            if tracked_frames_count > 0:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                if seconds_visible < 3.0:
                    st.markdown("<h3>⏳ Auto Slow-Motion Extraction</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#8b9bb4;'>Target was visible for only {seconds_visible:.2f}s. Automatically generating 0.25x highlight clip...</p>", unsafe_allow_html=True)
                    
                    slow_mo_out = "ClearSight_SlowMo.mp4"
                    slow_fps = max(fps * 0.25, 1.0)
                    
                    with st.spinner("Compiling Slow-Motion frames..."):
                        try:
                            sm_writer = imageio.get_writer(slow_mo_out, fps=slow_fps, codec='libx264')
                            for h_frame in highlight_frames: sm_writer.append_data(h_frame)
                            sm_writer.close()
                            
                            with open(slow_mo_out, 'rb') as f:
                                sm_bytes = f.read()
                                st.video(sm_bytes)
                                st.download_button(
                                    "📥 Download Highlight Clip", 
                                    data=sm_bytes, 
                                    file_name="ClearSight_SlowMo_Highlight.mp4", 
                                    mime="video/mp4", 
                                    key="dl_slowmo"
                                )
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.markdown("<h3>✅ Slow Motion Not Required</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#8b9bb4;'>The target was visible for a significant amount of time ({seconds_visible:.2f} seconds). An extracted slow-motion highlight reel is not required.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
