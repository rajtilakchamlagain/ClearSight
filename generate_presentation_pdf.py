import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

def generate_script_pdf():
    print("Generating Comprehensive Presentation Script PDF...")
    doc = SimpleDocTemplate("ClearSight_Presentation_Script.pdf", pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=26, alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor("#0f2027"))
    h1_style = ParagraphStyle('H1Style', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#203a43"), spaceBefore=20, spaceAfter=10)
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor("#2c5364"), spaceBefore=15, spaceAfter=10)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=18, alignment=TA_JUSTIFY, spaceAfter=10)
    code_style = ParagraphStyle('CodeStyle', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=11, textColor=colors.darkblue, backColor=colors.HexColor("#F0F0F0"), borderPadding=8, spaceBefore=5, spaceAfter=5)
    speech_style = ParagraphStyle('SpeechStyle', parent=styles['Normal'], fontName='Times-Italic', fontSize=14, leading=20, textColor=colors.HexColor("#333333"), spaceBefore=10, spaceAfter=10)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=18, spaceAfter=5, textColor=colors.HexColor("#111111"))

    Story = []

    # --- TITLE PAGE ---
    Story.append(Spacer(1, 100))
    Story.append(Paragraph("CLEARSIGHT AI: THE ULTIMATE PRESENTATION SCRIPT", title_style))
    Story.append(Spacer(1, 30))
    Story.append(Paragraph("Complete Step-by-Step Speech & Code Explanation Guide<br/>For Raj Tilak Chamlagain", ParagraphStyle('SubTitle', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER, leading=22)))
    Story.append(PageBreak())

    # --- SECTION 1: THE ELI5 (Nursery Kid) ---
    Story.append(Paragraph("PART 1: The 'Explain it to a Child' Analogy", h1_style))
    Story.append(Paragraph("Start your presentation by explaining the system in a way that absolutely anyone can understand:", body_style))
    
    eli5_speech = (
        "\"Imagine you want to find your friend in a massive, crowded stadium, and you only have one photo of them. "
        "Our AI acts like a team of three super-smart security guards passing information down a line.<br/><br/>"
        "1. First is the Detective (MTCNN). The Detective's only job is to scan the stadium with binoculars and draw a box around every single face they see. They ignore trees, clothes, and the stadium itself.<br/><br/>"
        "2. Next, the Detective passes the picture of the face to the Photoshop Artist (CLAHE). The stadium is dark and shadowy, making it hard to see the face clearly. The Artist magically brightens up the face, removes shadows, and makes every feature perfectly clear.<br/><br/>"
        "3. Finally, the picture is given to the Mathematician (FaceNet). The Mathematician doesn't see a picture; they pull out a ruler and take 512 exact measurements of the face—like the distance between the eyes. They create a secret mathematical password. If someone walks past the camera and their face's password matches your friend's password, the system locks on and alerts us!\""
    )
    Story.append(Paragraph(eli5_speech, speech_style))

    # --- SECTION 2: THE PROFESSIONAL EXPLANATION ---
    Story.append(Paragraph("PART 2: The 'Professional AI Engineer' Speech", h1_style))
    Story.append(Paragraph("When it is time to get serious, explain your architecture like this:", body_style))
    
    prof_speech = (
        "\"To build ClearSight, I engineered a highly optimized, 3-stage computer vision pipeline designed for Zero-Shot tracking in unconstrained CCTV environments.<br/><br/>"
        "First, I utilized MTCNN (Multi-task Cascaded Convolutional Networks) for facial detection. MTCNN is vastly superior to older algorithms like Haar Cascades because it uses three cascading neural networks to filter out false positives and accurately detect faces even at severe angles.<br/><br/>"
        "Second, and arguably the most crucial step for real-world deployment, is the CLAHE processor. CCTV footage is notorious for poor lighting. Before any face is sent for verification, I pass it through a Contrast Limited Adaptive Histogram Equalization (CLAHE) algorithm. This acts as a localized contrast filter, algorithmically rescuing facial landmarks hidden in deep shadows without amplifying digital noise.<br/><br/>"
        "Finally, the perfectly illuminated facial tensor is routed through FaceNet (InceptionResnetV1). This model uses Triplet Loss to map human faces onto a 512-dimensional Euclidean hypersphere. By calculating the physical geometric distance between the live CCTV face and our target's master embedding, I can achieve instantaneous tracking with extreme precision.\""
    )
    Story.append(Paragraph(prof_speech, speech_style))

    Story.append(PageBreak())

    # --- SECTION 3: KEYWORD DEFINITIONS ---
    Story.append(Paragraph("PART 3: Defending the Difficult Terms", h1_style))
    Story.append(Paragraph("Make sure you understand exactly what these terms mean before you present:", body_style))
    
    Story.append(Paragraph("What is 'Zero-Shot Learning'?", bold_style))
    Story.append(Paragraph("Traditional AI (like YOLO) uses 'Many-Shot' learning. If you want the AI to recognize a dog, you have to train it on 10,000 photos of dogs. If you want it to recognize 'Raj', you must give it 10,000 photos of Raj and train it for hours. <b>Zero-Shot Learning</b> means the AI is so smart at measuring faces that it does NOT need to be trained on the target. You give it <i>one</i> photo at runtime, and it instantly recognizes the person. It has 'Zero' prior training on that specific identity.", body_style))

    Story.append(Paragraph("What is 'CLAHE' (The Middle Step)?", bold_style))
    Story.append(Paragraph("CLAHE stands for <i>Contrast Limited Adaptive Histogram Equalization</i>. Normal photo brightening tools brighten the whole image, which washes it out. CLAHE divides the face into a grid of tiny 8x8 squares. It balances the lighting inside each square individually, and then stitches them back together. This perfectly fixes faces hidden in shadows.", body_style))

    Story.append(Paragraph("What is 'Euclidean Distance' and the 0.85 Threshold?", bold_style))
    Story.append(Paragraph("FaceNet turns a face into a list of 512 numbers (coordinates on a graph). Euclidean Distance is the straight-line math formula to measure how far apart two faces are on that graph. A distance of 0.0 means the faces are perfectly identical. Through testing, I found that setting the threshold to exactly <b>0.85</b> perfectly balances catching the target while ignoring strangers.", body_style))

    Story.append(PageBreak())

    # --- SECTION 4: EXPLAINING YOUR EXACT CODE ---
    Story.append(Paragraph("PART 4: Breaking Down Your Python Code", h1_style))
    Story.append(Paragraph("If the professor points to a specific line in your code and asks what it does, use this guide:", body_style))

    Story.append(Paragraph("1. The CLAHE Illumination Fixer", h2_style))
    Story.append(Paragraph("def get_perfect_face(img_rgb, face):<br/>&nbsp;&nbsp;&nbsp;&nbsp;...<br/>&nbsp;&nbsp;&nbsp;&nbsp;lab = cv2.cvtColor(face_crop, cv2.COLOR_RGB2LAB)<br/>&nbsp;&nbsp;&nbsp;&nbsp;l, a, b = cv2.split(lab)<br/>&nbsp;&nbsp;&nbsp;&nbsp;cl = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)<br/>&nbsp;&nbsp;&nbsp;&nbsp;return cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2RGB)", code_style))
    Story.append(Paragraph("<b>What you say:</b> 'This is the middle step. I convert the cropped face from RGB colors to LAB colors. The 'L' stands for Lightness. I apply the CLAHE algorithm only to the 'L' channel to fix the shadows, and then merge the colors back together. This gives FaceNet a perfectly lit image.'", body_style))

    Story.append(Paragraph("2. The Twin Mode vs Normal Mode Logic", h2_style))
    Story.append(Paragraph("if cond_resp == '2':<br/>&nbsp;&nbsp;&nbsp;&nbsp;REQUIRED_FRAMES = 1<br/>&nbsp;&nbsp;&nbsp;&nbsp;EUCLIDEAN_THRESHOLD = 0.87<br/>else:<br/>&nbsp;&nbsp;&nbsp;&nbsp;REQUIRED_FRAMES = 5<br/>&nbsp;&nbsp;&nbsp;&nbsp;EUCLIDEAN_THRESHOLD = 0.85", code_style))
    Story.append(Paragraph("<b>What you say:</b> 'I built a dynamic configuration engine. If the CCTV is high quality, I use strict bank-vault math (0.85 threshold) and require the AI to see the person for 5 consecutive frames before locking on. But if the camera is shaky or blurry, I make the math more forgiving (0.87 threshold) and lock on instantly after 1 frame.'", body_style))

    Story.append(Paragraph("3. The Verification Math", h2_style))
    Story.append(Paragraph("target_tensor = preprocess(enhanced_rgb).unsqueeze(0).to(device)<br/>with torch.no_grad():<br/>&nbsp;&nbsp;&nbsp;&nbsp;target_embedding = resnet(target_tensor)<br/>distance = torch.dist(master_embedding, target_embedding).item()", code_style))
    Story.append(Paragraph("<b>What you say:</b> 'This is the core engine. I convert the image into a PyTorch Tensor and push it to the GPU (`to(device)`). I use `torch.no_grad()` to freeze the GPU's memory so it doesn't waste time trying to learn, giving me maximum FPS. Finally, I pass it through FaceNet (`resnet`) and calculate the physical distance between the master password and the live face.'", body_style))

    Story.append(Paragraph("4. The Tracker Handoff", h2_style))
    Story.append(Paragraph("if is_locked and tracker is not None:<br/>&nbsp;&nbsp;&nbsp;&nbsp;success, bbox = tracker.update(frame_bgr)", code_style))
    Story.append(Paragraph("<b>What you say:</b> 'Once the AI gets 5 consecutive math locks, it shuts down the heavy FaceNet calculations and hands the tracking over to a lightweight OpenCV CSRT Tracker. This saves a massive amount of computational power, as the system just follows the physical pixel-box instead of calculating 512 dimensions every single frame.'", body_style))

    doc.build(Story)
    print("DONE! Comprehensive script generated.")

if __name__ == "__main__":
    generate_script_pdf()
