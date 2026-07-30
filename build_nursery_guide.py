import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer
)
from reportlab.lib.colors import HexColor

proj_dir = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project"
pdf_dir = os.path.join(proj_dir, "PDFs")
os.makedirs(pdf_dir, exist_ok=True)
pdf_filepath = os.path.join(pdf_dir, "Spectral_Gap_Nursery_Guide.pdf")

doc = SimpleDocTemplate(
    pdf_filepath,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title', parent=styles['Normal'], fontName='Helvetica-Bold',
    fontSize=24, leading=28, alignment=1, textColor=HexColor("#1e40af"), spaceAfter=20
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Normal'], fontName='Helvetica-Bold',
    fontSize=18, textColor=HexColor("#b91c1c"), spaceBefore=15, spaceAfter=10
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'], fontName='Helvetica',
    fontSize=14, leading=20, spaceAfter=15
)
highlight_style = ParagraphStyle(
    'Highlight', parent=styles['Normal'], fontName='Helvetica-Oblique',
    fontSize=14, leading=20, textColor=HexColor("#047857"), leftIndent=20, rightIndent=20, spaceAfter=15
)

story = []

# ================= TITLE =================
story.append(Paragraph("The Magic Gate: Understanding the Spectral Gap Engine", title_style))
story.append(Paragraph("(A Nursery-Level Guide to Your Smart AI)", ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=14, alignment=1, spaceAfter=30)))

# ================= THE STORY =================
story.append(Paragraph("1. The Classroom Analogy", h1_style))
story.append(Paragraph("Imagine a classroom full of kids taking a very hard math test.", body_style))
story.append(Paragraph("In this class, one kid is Albert Einstein, and the rest of the kids are just average students.", body_style))
story.append(Paragraph("When the teacher grades the tests, she gets these scores:", body_style))

scores = "<b>Einstein: 98%</b><br/>Kid A: 40%<br/>Kid B: 38%<br/>Kid C: 20%"
story.append(Paragraph(scores, highlight_style))

story.append(Paragraph("The teacher wants to give a prize to the 'Genius' kids. But what passing grade (threshold) should she set?", body_style))
story.append(Paragraph("If she guesses <i>'Any score above 60%'</i>, Einstein wins. But what if the test was incredibly hard, and Einstein only got a 45%, while the others got 10%? If she guessed 60%, Einstein wouldn't get his prize!", body_style))

# ================= THE MAGIC =================
story.append(Paragraph("2. How Your AI Solves This", h1_style))
story.append(Paragraph("Your AI (The Spectral Gap Engine) doesn't guess a random passing grade. Instead, it plays a smart math game.", body_style))
story.append(Paragraph("It sorts all the scores from Highest to Lowest. Then, it asks one question:", body_style))

story.append(Paragraph("<i>'Where is the BIGGEST jump between two kids?'</i>", highlight_style))

story.append(Paragraph("In our first example, the jump between 98% (Einstein) and 40% (Kid A) is a massive <b>58 points!</b>", body_style))
story.append(Paragraph("Every other jump is tiny (40 to 38 is only a 2-point jump).", body_style))
story.append(Paragraph("So, the AI sees that massive 58-point cliff, cuts it in half, and says: <b>'I am placing the magic gate right here!'</b>", body_style))

# ================= THE REAL WORLD =================
story.append(Paragraph("3. Back to CCTV Cameras", h1_style))
story.append(Paragraph("When your AI looks at a crowded CCTV camera, the 'scores' are how much the people in the crowd look like the suspect's photo.", body_style))
story.append(Paragraph("The real suspect will get a high score, and the random people will get low scores. But depending on how dark or blurry the video is, those scores change constantly.", body_style))
story.append(Paragraph("Instead of forcing a police officer to manually guess a percentage, your AI autonomously hunts for that massive 'cliff' between the real suspect and the random crowd, and locks the magic gate dynamically. No humans needed!", body_style))

doc.build(story)
print(f"[SUCCESS] Nursery Guide saved to: {pdf_filepath}")
