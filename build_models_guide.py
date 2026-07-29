import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)

proj_dir = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project"
pdf_dir = os.path.join(proj_dir, "PDFs")
os.makedirs(pdf_dir, exist_ok=True)
pdf_filepath = os.path.join(pdf_dir, "ClearSight_Models_Explanation_Guide.pdf")

doc = SimpleDocTemplate(
    pdf_filepath,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch
)

styles = getSampleStyleSheet()

COLOR_PRIMARY = colors.HexColor("#1e293b")
COLOR_HEADING = colors.HexColor("#0f172a")
COLOR_ACCENT = colors.HexColor("#2563eb")
COLOR_ALERT = colors.HexColor("#dc2626")

title_style = ParagraphStyle(
    'Title', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=22, leading=26,
    alignment=1, textColor=COLOR_HEADING, spaceAfter=20
)

h1_style = ParagraphStyle(
    'H1', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=16, leading=22,
    textColor=COLOR_ACCENT, spaceBefore=20, spaceAfter=10
)

h2_style = ParagraphStyle(
    'H2', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=14, leading=18,
    textColor=COLOR_HEADING, spaceBefore=15, spaceAfter=8
)

h3_style = ParagraphStyle(
    'H3', parent=styles['Normal'],
    fontName='Helvetica-BoldOblique', fontSize=12, leading=16,
    textColor=COLOR_ALERT, spaceBefore=10, spaceAfter=6
)

body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontName='Helvetica', fontSize=11, leading=16,
    alignment=4, textColor=COLOR_PRIMARY, spaceAfter=10 # Justified
)

bullet_style = ParagraphStyle(
    'Bullet', parent=body_style, leftIndent=20, firstLineIndent=-10, spaceAfter=5
)

story = []

# ================= COVER =================
story.append(Paragraph("ClearSight AI:<br/>Kiddy-Style Guide to Models Used", title_style))
story.append(Spacer(1, 10))
story.append(Paragraph("A comprehensive, easy-to-understand breakdown of every deep learning model and algorithm used in the ClearSight project, including why we used them and why we rejected alternatives.", body_style))
story.append(Spacer(1, 20))

story.append(Paragraph("List of Models & Algorithms Used:", h2_style))
story.append(Paragraph("• <b>YOLOv8:</b> For finding human bodies (Bounding Boxes).", bullet_style))
story.append(Paragraph("• <b>ByteTrack:</b> For tracking humans over time (Even when they hide).", bullet_style))
story.append(Paragraph("• <b>RetinaFace:</b> For finding the exact points of a face (Eyes, Nose, Mouth).", bullet_style))
story.append(Paragraph("• <b>ArcFace:</b> For comparing faces mathematically (512D Vector ID).", bullet_style))
story.append(Paragraph("• <b>Autonomous Spectral Gap Engine:</b> For deciding when a match is real without humans guessing.", bullet_style))
story.append(PageBreak())

# ================= YOLOv8 =================
story.append(Paragraph("1. YOLOv8 (You Only Look Once)", h1_style))
story.append(Paragraph("What is it?", h2_style))
story.append(Paragraph("Imagine you are looking at a picture and instantly drawing a box around every person you see in one quick glance. That is what YOLOv8 does. It is a super-fast Artificial Intelligence that 'looks' at an image once and tells you exactly where all the people are by drawing a bounding box around them.", body_style))

story.append(Paragraph("How is it used in general?", h2_style))
story.append(Paragraph("It is used in self-driving cars to spot pedestrians, in security cameras to detect intruders, and in factories to spot defective items on a conveyor belt. It's famous because it is incredibly fast (real-time).", body_style))

story.append(Paragraph("How did YOU use it?", h2_style))
story.append(Paragraph("In ClearSight AI, I used YOLOv8 as the very first step. Before I can recognize a face, I need to know where the people are in the crowded video. YOLOv8 scans every single frame of the surveillance video and draws boxes around all the pedestrians walking around.", body_style))

story.append(Paragraph("Architecture (Simply Explained)", h2_style))
story.append(Paragraph("YOLOv8 uses a 'Convolutional Neural Network' (CNN). Think of it as a series of filters. The first filter looks for simple edges, the next looks for shapes like circles, and the final filters recognize a human body. It divides the image into a grid and guesses if there is a person inside each grid cell, all in a single forward pass—hence 'You Only Look Once'.", body_style))

story.append(Paragraph("Why didn't we use alternatives like Faster R-CNN or SSD?", h3_style))
story.append(Paragraph("Faster R-CNN is like a slow, careful detective. It first proposes a thousand possible locations, then checks each one. It is very accurate but way too slow for live video. SSD (Single Shot Detector) is faster but older and struggles with small objects (like people far away in CCTV). YOLOv8 gives us the perfect balance of blazing speed and high accuracy.", body_style))
story.append(PageBreak())

# ================= ByteTrack =================
story.append(Paragraph("2. ByteTrack (Kinetic Tracker)", h1_style))
story.append(Paragraph("What is it?", h2_style))
story.append(Paragraph("YOLOv8 only finds people in one single picture. If you give it a video, it treats every frame as a brand-new picture and forgets the person from the previous frame. ByteTrack is the 'memory'. It connects the boxes across frames. If Box A in Frame 1 moves slightly to the right in Frame 2, ByteTrack says, 'Ah! That is the same person, let's call him Person #1.'", body_style))

story.append(Paragraph("How is it used in general?", h2_style))
story.append(Paragraph("It is used in sports analytics to track football players running across a field, or in traffic cameras to track the speed of cars without mixing them up.", body_style))

story.append(Paragraph("How did YOU use it?", h2_style))
story.append(Paragraph("In crowded CCTV footage, people constantly walk behind pillars or other people (occlusion). When a person hides behind a pillar, YOLOv8 loses them. ByteTrack uses math to predict where they will come out. When the person reappears, ByteTrack remembers them and gives them their original ID back instead of treating them as a new stranger.", body_style))

story.append(Paragraph("Architecture (Simply Explained)", h2_style))
story.append(Paragraph("ByteTrack relies on something called a 'Kalman Filter'. A Kalman Filter is just a math formula that predicts future movement based on past speed and direction. If a person is walking right at 5 km/h, the Kalman Filter predicts they will be slightly further right in the next second. ByteTrack also intelligently recycles 'low-confidence' YOLO boxes (blurry boxes that other trackers throw away) to keep the track alive.", body_style))

story.append(Paragraph("Why didn't we use alternatives like DeepSORT?", h3_style))
story.append(Paragraph("DeepSORT is a very famous old tracker. But DeepSORT relies heavily on how the person looks (their shirt color, etc.) to track them. In crowded, dark CCTV, colors change and get blurry, so DeepSORT gets confused and drops the ID. ByteTrack relies more on spatial movement (Intersection over Union - IoU) and keeps tracking even when the camera is black-and-white or blurry.", body_style))
story.append(PageBreak())

# ================= RetinaFace =================
story.append(Paragraph("3. RetinaFace (Facial Landmark Detector)", h1_style))
story.append(Paragraph("What is it?", h2_style))
story.append(Paragraph("Once YOLOv8 finds the human body, we zoom in on the head. RetinaFace is a specialized model that finds the exact coordinates of the 5 key facial landmarks: Left Eye, Right Eye, Nose Tip, Left Mouth Corner, and Right Mouth Corner.", body_style))

story.append(Paragraph("How is it used in general?", h2_style))
story.append(Paragraph("Snapchat and Instagram filters use similar landmark detectors to know exactly where to place virtual dog ears or glasses on your face.", body_style))

story.append(Paragraph("How did YOU use it?", h2_style))
story.append(Paragraph("I used RetinaFace to 'straighten' the face. When people walk in CCTV, their heads are tilted. If you try to compare a tilted face to a straight passport photo, the computer fails. RetinaFace finds the eyes, and then I use a math trick (Affine Transformation) to rotate and warp the face so the eyes are perfectly level before sending it to the recognition model.", body_style))

story.append(Paragraph("Architecture (Simply Explained)", h2_style))
story.append(Paragraph("RetinaFace uses a 'Feature Pyramid Network'. Imagine looking at a face through a magnifying glass. The network looks at the face at multiple zoom levels—zoomed out to find the general face box, and zoomed in to find tiny pixel details like the pupil of the eye. It predicts everything (box, face score, and 5 points) all at once.", body_style))

story.append(Paragraph("Why didn't we use alternatives like MTCNN, Haar Cascades, or Dlib?", h3_style))
story.append(Paragraph("Haar Cascades (the old green boxes on digital cameras) are terrible; they only work on bright, perfectly straight faces. Dlib is slow and struggles with side-profiles. MTCNN is popular but it uses 3 separate neural networks in a cascade (P-Net, R-Net, O-Net), which makes it very slow. RetinaFace is a modern single-stage detector that can find tiny, dark, side-profile faces instantly.", body_style))
story.append(PageBreak())

# ================= ArcFace =================
story.append(Paragraph("4. ArcFace (Facial Recognition Encoder)", h1_style))
story.append(Paragraph("What is it?", h2_style))
story.append(Paragraph("ArcFace is the brain that actually 'remembers' faces. Instead of saving a picture of a face, it converts a face into a list of 512 numbers (a 512-Dimensional Vector). This list of numbers is like a unique mathematical fingerprint for that person's face.", body_style))

story.append(Paragraph("How is it used in general?", h2_style))
story.append(Paragraph("It is used in airport e-gates for passport verification and in your smartphone's Face Unlock feature.", body_style))

story.append(Paragraph("How did YOU use it?", h2_style))
story.append(Paragraph("I feed the straight, cropped face (from RetinaFace) into ArcFace. ArcFace spits out 512 numbers. I do this for the Target Suspect's photo, and I do it for the people walking in the CCTV. Then, I just compare the two lists of numbers using high-school trigonometry (Cosine Similarity). If the angle between the two lists of numbers is very small, it's the exact same person!", body_style))

story.append(Paragraph("Architecture (Simply Explained)", h2_style))
story.append(Paragraph("ArcFace is built on top of a deep 'ResNet-50' neural network. ResNet uses 'skip connections' that allow it to be 50 layers deep without forgetting what it learned in the first layer. The true magic of ArcFace is its 'Additive Angular Margin Loss'. During training, it forces pictures of the same person to cluster tightly together on a mathematical sphere, and pushes pictures of different people far apart by a strict angular margin.", body_style))

story.append(Paragraph("Why didn't we use alternatives like FaceNet or VGG-Face?", h3_style))
story.append(Paragraph("FaceNet (developed by Google) uses 'Triplet Loss'. Training Triplet Loss is a nightmare because you have to constantly feed it an Anchor (Suspect), a Positive (Same Suspect), and a Negative (Different Person). It's slow and outdated. ArcFace is the modern king because its angular math naturally creates massive separation between different identities, making it insanely accurate even if the suspect aged 10 years or grew a beard.", body_style))
story.append(PageBreak())

# ================= Why No GenAI / CLAHE =================
story.append(Paragraph("5. The Rule of Law: Why No GenAI or CLAHE?", h1_style))
story.append(Paragraph("What are they?", h2_style))
story.append(Paragraph("<b>GenAI (Generative AI like GFPGAN, Midjourney):</b> AI that hallucinates or creates new pixels to make a blurry image look sharp and beautiful in 4K.<br/><br/><b>CLAHE (Contrast Limited Adaptive Histogram Equalization):</b> A traditional image processing tool that forces dark shadows to become bright by stretching the color pixels.", body_style))

story.append(Paragraph("Why didn't we use them?", h3_style))
story.append(Paragraph("ClearSight AI is a digital forensic tool meant for law enforcement and courtrooms. If you take a blurry CCTV photo of a suspect and use GenAI (GFPGAN) to make it sharp, the AI is literally <b>guessing and inventing fake pixels</b> that were never captured by the camera. It might hallucinate a scar or change the shape of the nose.", body_style))
story.append(Paragraph("If you present an AI-enhanced photo in a court of law, the defense lawyer will immediately object: <i>'Your Honor, this photo is manipulated. The AI invented my client's face.'</i> The judge will throw out the evidence.", body_style))
story.append(Paragraph("The same applies to CLAHE. Aggressive color stretching corrupts the original pixel integrity. In digital forensics, we MUST respect the original pixels. Our deep learning pipeline (ArcFace + RetinaFace) is trained to natively handle dark, blurry, low-resolution pixels directly, proving that we do not need to manipulate or 'enhance' the evidence to make a positive identification.", body_style))

# ================= The Spectral Gap Engine =================
story.append(Paragraph("6. The Autonomous Spectral Gap Engine", h1_style))
story.append(Paragraph("What is it?", h2_style))
story.append(Paragraph("This is not a deep learning neural network, but a custom mathematical algorithm I built for this project. When comparing faces, the system gets match scores (like 85%, 60%, 20%). Normally, a human operator has to guess a threshold (e.g., 'Anything above 50% is a match!'). My Spectral Gap Engine removes the human from the equation.", body_style))

story.append(Paragraph("How did YOU use it?", h2_style))
story.append(Paragraph("The algorithm takes all the match scores in the scene, sorts them from highest to lowest, and subtracts them from each other to find the biggest drop-off (the 'cliff'). If the scores are [90%, 88%, 85%, 20%, 18%], the algorithm finds the massive gap between 85% and 20%, and automatically places the threshold at 52%. It autonomously separates the suspect from the crowd without human bias.", body_style))

doc.build(story)
print(f"[SUCCESS] Saved Models Guide to {pdf_filepath}")
