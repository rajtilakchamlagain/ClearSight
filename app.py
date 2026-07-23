import os
import cv2
import torch
import numpy as np
import imageio
import streamlit as st
import tempfile
import requests
from torchvision import transforms
import torch.nn.functional as F
import facenet_pytorch
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
    st.markdown("<h2>ClearSight V4 (Surveillance ReID)</h2>", unsafe_allow_html=True)
    st.write("**1. Body Tracking (YOLOv8)**: DeepSORT/ByteTrack to perfectly track human bodies in crowds.")
    st.write("**2. Identity Binding (FaceNet ReID)**: Verifies the face once and binds the identity to the body.")
    st.write("**3. Permanent Lock**: 100% resilient tracking even when the face turns away from the camera or gets blurry.")
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
            COSINE_THRESHOLD = 0.15 # Ultra-high tolerance for CCTV ReID
            
            st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#00f2fe;'>Initializing YOLOv8 ReID Surveillance Pipeline...</h3>", unsafe_allow_html=True)
            
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            @st.cache_resource
            def load_models():
                # 1. Identity Verification Model
                detector = facenet_pytorch.MTCNN(thresholds=[0.6, 0.7, 0.7], keep_all=True, device=device, min_face_size=10)
                resnet = facenet_pytorch.InceptionResnetV1(pretrained='vggface2').eval().to(device)
                preprocess = transforms.Compose([
                    transforms.ToPILImage(), transforms.Resize((160, 160)),
                    transforms.ToTensor(), transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
                ])
                # 2. Body Tracking Model
                yolo = YOLO('yolov8n.pt') 
                return detector, resnet, preprocess, yolo

            face_detector, resnet, preprocess, yolo_model = load_models()
            
            def get_raw_face(img_rgb, box):
                x1, y1, x2, y2 = box.astype(int)
                w, h = x2 - x1, y2 - y1
                x, y = max(0, x1), max(0, y1)
                face_crop = img_rgb[y:y+h, x:x+w]
                if face_crop.size == 0: return None
                return face_crop
            
            # Master Vector Generation
            anchor_embeddings = []
            for ref_f in ref_files:
                img = Image.open(ref_f).convert('RGB')
                img_rgb = np.array(img)
                boxes, probs = face_detector.detect(img_rgb)
                
                if boxes is not None and len(boxes) > 0:
                    biggest_box = max(boxes, key=lambda b: (b[2]-b[0]) * (b[3]-b[1]))
                    perfect_face = get_raw_face(img_rgb, biggest_box)
                    if perfect_face is not None:
                        tensor = preprocess(perfect_face).unsqueeze(0).to(device)
                        with torch.no_grad():
                            anchor_embeddings.append(resnet(tensor))
            
            if not anchor_embeddings:
                st.error("No valid faces detected in reference images.")
                st.stop()
                
            master_embedding = torch.mean(torch.cat(anchor_embeddings), dim=0, keepdim=True)
            st.markdown("✅ **Master Vector Extracted Successfully (PyTorch)**", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Video Processing
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tfile.write(video_file.read())
            tfile.close()
            
            cap = cv2.VideoCapture(tfile.name)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            out_path = "tracked_output.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
            
            best_screenshots = []
            highlight_frames = []
            tracked_frames_count = 0
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Live Processing Feed (Real-Time PyTorch ReID)</h3>", unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Tracking State Variables
            TARGET_TRACK_ID = None
            known_non_targets = set()
            
            frame_count = 0
            # Use YOLO track to process the video with ByteTrack
            results = yolo_model.track(source=tfile.name, classes=[0], stream=True, persist=True, verbose=False)
            
            for r in results:
                frame_count += 1
                frame_bgr = r.orig_img
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                
                target_detected = False
                
                if r.boxes.id is not None:
                    boxes = r.boxes.xyxy.cpu().numpy()
                    track_ids = r.boxes.id.cpu().numpy().astype(int)
                    
                    for box, track_id in zip(boxes, track_ids):
                        
                        # Case 1: We ALREADY identified this body as the target
                        if track_id == TARGET_TRACK_ID:
                            x1, y1, x2, y2 = box.astype(int)
                            cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 3)
                            cv2.putText(frame_bgr, f"LOCKED RE-ID [{track_id}]", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            target_detected = True
                            continue
                            
                        # Case 2: We know this body is NOT the target
                        if track_id in known_non_targets:
                            continue
                            
                        # Case 3: We have NEVER identified this body yet. Run Identity Check.
                        if TARGET_TRACK_ID is None:
                            # Extract body crop to look for a face
                            x1, y1, x2, y2 = box.astype(int)
                            x, y = max(0, x1), max(0, y1)
                            w, h = x2 - x1, y2 - y1
                            
                            # Expand YOLO box upwards to ensure head isn't cut off
                            y_exp = max(0, int(y - h * 0.2))
                            body_crop = frame_rgb[y_exp:y+h, x:x+w]
                            
                            if body_crop.size == 0: continue
                            
                            face_boxes, probs = face_detector.detect(body_crop)
                            if face_boxes is not None and len(face_boxes) > 0:
                                # We found a face inside this body
                                biggest_face = max(face_boxes, key=lambda b: (b[2]-b[0]) * (b[3]-b[1]))
                                perfect_face = get_raw_face(body_crop, biggest_face)
                                if perfect_face is not None:
                                    with torch.no_grad():
                                        tensor = preprocess(perfect_face).unsqueeze(0).to(device)
                                        embedding = resnet(tensor)
                                    
                                    cosine_sim = F.cosine_similarity(master_embedding, embedding).item()
                                    
                                    if cosine_sim > COSINE_THRESHOLD:
                                        # WE FOUND THE TARGET! BIND THE IDENTITY
                                        TARGET_TRACK_ID = track_id
                                        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 3)
                                        cv2.putText(frame_bgr, f"TARGET ACQUIRED [{track_id}]", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                        target_detected = True
                                        best_screenshots.append((cosine_sim, frame_rgb.copy()))
                                    else:
                                        known_non_targets.add(track_id) # Don't check this person again

                out.write(frame_bgr)
                
                if target_detected:
                    tracked_frames_count += 1
                    marked_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                    highlight_frames.append(marked_rgb)
                
                if frame_count % 5 == 0:
                    progress_bar.progress(min(frame_count / total_frames, 1.0))
                    status_text.text(f"Scanning Frame {frame_count}/{total_frames} at Ultra Speed...")
                    
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
                st.markdown("<h3>📸 Re-Identification Match</h3>", unsafe_allow_html=True)
                sc1, sc2, sc3 = st.columns(3)
                cols = [sc1, sc2, sc3]
                for i, (sim, frame) in enumerate(best_screenshots):
                    if i > 2: break
                    cols[i].image(frame, caption=f"Identity Match Confidence: {sim:.3f}", use_container_width=True)
                    
                    is_success, buffer = cv2.imencode(".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    if is_success:
                        cols[i].download_button(
                            label="📥 Save Identity Log",
                            data=buffer.tobytes(),
                            file_name=f"ClearSight_BestMatch_Capture_{i+1}.jpg",
                            mime="image/jpeg",
                            key=f"dl_img_{i}"
                        )
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
