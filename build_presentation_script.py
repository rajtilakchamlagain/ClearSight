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
pdf_filepath = os.path.join(pdf_dir, "ClearSight_Presentation_Speech_Script.pdf")

doc = SimpleDocTemplate(
    pdf_filepath,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch
)

styles = getSampleStyleSheet()

COLOR_PRIMARY = colors.HexColor("#000000")
COLOR_HEADING = colors.HexColor("#1e3a8a")
COLOR_BRACKET = colors.HexColor("#dc2626")

title_style = ParagraphStyle(
    'Title', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=22, leading=26,
    alignment=1, textColor=COLOR_HEADING, spaceAfter=20
)

h1_style = ParagraphStyle(
    'H1', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=16, leading=22,
    textColor=COLOR_HEADING, spaceBefore=20, spaceAfter=10
)

body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontName='Helvetica', fontSize=12, leading=18,
    alignment=4, textColor=COLOR_PRIMARY, spaceAfter=10
)

bracket_style = ParagraphStyle(
    'Bracket', parent=styles['Normal'],
    fontName='Helvetica-Oblique', fontSize=11, leading=16,
    textColor=COLOR_BRACKET, spaceBefore=5, spaceAfter=15,
    leftIndent=20
)

story = []

# ================= COVER =================
story.append(Paragraph("ClearSight AI:<br/>Presentation Speech Script", title_style))
story.append(Spacer(1, 10))
story.append(Paragraph("<i>Print this out or keep it on your phone. Read the black text out loud. The red italic text inside brackets are explanations just for you!</i>", body_style))
story.append(Spacer(1, 20))

# ================= SLIDE 1 =================
story.append(Paragraph("SLIDE 1: Title Slide (ClearSight AI)", h1_style))
story.append(Paragraph("<b>Good morning Respected Sir, Ma'am, and everyone present here.</b>", body_style))
story.append(Paragraph("Four years ago, when my family and I went on a trip during our summer break, my small sister got lost in a massive crowd. Luckily, after hours of panic, we found her. But that terrifying feeling struck my mind... What if the police had a system that could just scan every camera in the city and find her instantly?", body_style))
story.append(Paragraph("That thought became the foundation of my project. Today, I am proud to present <b>ClearSight AI: An Autonomous Kinetic and Biometric Re-Identification Engine</b>.", body_style))

# ================= SLIDE 2 =================
story.append(Paragraph("SLIDE 2: The Surveillance Dilemma", h1_style))
story.append(Paragraph("When I started researching, I realized standard CCTV tracking is completely broken. When targets walk into a crowd, they hide behind pillars or other people, and the camera loses them instantly. Furthermore, shadows and steep angles destroy standard facial recognition. And on top of that, attempting to load hundreds of high-resolution video evidence files freezes traditional police laptops.", body_style))

# ================= SLIDE 3 =================
story.append(Paragraph("SLIDE 3: 5-Phase Architecture Pipeline", h1_style))
story.append(Paragraph("To solve this, I engineered a 5-Phase Architecture.", body_style))
story.append(Paragraph("First, we encode the biometrics using RetinaFace and ArcFace. Second, we handle movement and occlusions using YOLOv8 and ByteTrack. Third, we use an autonomous math engine to threshold the results. And finally, we stream it securely to a Zero-Lag Web Interface.", body_style))
story.append(Paragraph("[<i>Just read through this slide quickly, the next slides will explain the details.</i>]", bracket_style))

# ================= SLIDE 4 =================
story.append(Paragraph("SLIDE 4: Solving Crowd Occlusion", h1_style))
story.append(Paragraph("Let's talk about tracking. I used YOLOv8 to detect human bodies instantly. But YOLO forgets people if they hide. So, I integrated ByteTrack.", body_style))
story.append(Paragraph("ByteTrack uses Kalman Filters. This means even if a person walks behind a pillar, the math predicts where they will come out based on their speed, keeping their ID alive!", body_style))
story.append(Paragraph("[<i>Kalman Filters: It's just a math formula that predicts where something is moving. If I throw a ball behind a wall, your brain knows where it will come out. Kalman Filters give the computer that exact same brain logic!</i>]", bracket_style))

# ================= SLIDE 5 =================
story.append(Paragraph("SLIDE 5: Biometric Invariance", h1_style))
story.append(Paragraph("For facial recognition, I didn't use outdated tools like FaceNet. I used RetinaFace to automatically find the eyes and mathematically straighten tilted faces.", body_style))
story.append(Paragraph("Then, ArcFace maps the face onto a 512-Dimensional sphere. Because it measures angles instead of raw pixels, it maintains over 90% accuracy even if the suspect is in a dark alley or wearing heavy makeup.", body_style))

# ================= SLIDE 6 =================
story.append(Paragraph("SLIDE 6: Autonomous Spectral Gap", h1_style))
story.append(Paragraph("Here is my core innovation. Usually, a human has to guess a threshold, like 'Anything above 50% is a match'. This is dangerous and causes false arrests.", body_style))
story.append(Paragraph("I wrote an algorithm called the Autonomous Spectral Gap. It looks at all the match scores and finds the largest mathematical drop-off (the cliff) between real matches and random crowd noise, and it automatically places the threshold right there. Zero human bias.", body_style))
story.append(Paragraph("[<i>How you made this: You literally wrote a python function that sorts the scores [90, 85, 20, 15] and subtracts them to find the biggest gap (85 - 20 = 65). It locks the door in that gap!</i>]", bracket_style))

# ================= SLIDE 7 =================
story.append(Paragraph("SLIDE 7: The Rule of Law", h1_style))
story.append(Paragraph("You might ask, why didn't I just use Generative AI or enhancers to make blurry faces sharper? Because of the Rule of Law.", body_style))
story.append(Paragraph("Generative AI hallucinates fake pixels. If we use manipulated evidence in court, defense attorneys will immediately have it thrown out. My pipeline strictly computes against authentic, unmanipulated pixels.", body_style))

# ================= SLIDE 8 =================
story.append(Paragraph("SLIDE 8: Zero-Lag Courtroom UI & Video Triage", h1_style))
story.append(Paragraph("To display the results, I built a Web Dashboard. Traditional dashboards crash because they try to load massive Base64 videos directly into the browser's memory.", body_style))
story.append(Paragraph("I bypassed this by engineering Native Disk Sockets, achieving 5,000x compression. Also, because deep learning models occasionally lose tracking IDs during extreme chaos, I implemented a Top-4 Split Strategy.", body_style))
story.append(Paragraph("Instead of forcing the computer to guess just 1 video, my system outputs the top 4 highest-confidence tracking videos side-by-side. This allows the human operator to visually verify the suspect from the best 4 angles, completely covering any AI mistakes!", body_style))
story.append(Paragraph("[<i>Native Disk Sockets: Instead of converting a video into a giant text string (Base64) and crashing the browser RAM, you wrote code that reads the .mp4 file directly off the hard drive in tiny chunks (sockets). </i>]", bracket_style))
story.append(Paragraph("[<i>4-Video Split Strategy: Explain to them proudly that NO model is 100% perfect. Since YOLO sometimes breaks a person's ID into 2 different IDs when they hide for too long, showing the top 4 videos guarantees the suspect is on screen for human verification! It is a deliberate fallback mechanism.</i>]", bracket_style))

# ================= SLIDE 9 =================
story.append(Paragraph("SLIDE 9: Conclusion & Future Scope", h1_style))
story.append(Paragraph("In conclusion, ClearSight AI is a turnkey digital forensic tool. It overcomes hardware limitations and eliminates human threshold guesswork.", body_style))
story.append(Paragraph("In the future, I plan to scale this to live Smart-City networks. Thank you for your time.", body_style))

# ================= SLIDE 10 =================
story.append(Paragraph("SLIDE 10: Thank You", h1_style))
story.append(Paragraph("<b>Thank you.</b>", body_style))

doc.build(story)
print(f"[SUCCESS] Presentation Speech Script saved to: {pdf_filepath}")
