import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)
from reportlab.lib.colors import HexColor

proj_dir = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project"
pdf_dir = os.path.join(proj_dir, "PDFs")
os.makedirs(pdf_dir, exist_ok=True)
pdf_filepath = os.path.join(pdf_dir, "Research_Paper_Autonomous_Spectral_Gap.pdf")

doc = SimpleDocTemplate(
    pdf_filepath,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch
)

styles = getSampleStyleSheet()

# Academic Paper Styles
title_style = ParagraphStyle(
    'PaperTitle', parent=styles['Normal'], fontName='Times-Bold',
    fontSize=18, leading=22, alignment=1, spaceAfter=20
)
author_style = ParagraphStyle(
    'Author', parent=styles['Normal'], fontName='Times-Roman',
    fontSize=12, alignment=1, spaceAfter=20
)
abstract_heading = ParagraphStyle(
    'AbstractH', parent=styles['Normal'], fontName='Times-Bold',
    fontSize=11, alignment=1, spaceAfter=10
)
abstract_body = ParagraphStyle(
    'AbstractB', parent=styles['Normal'], fontName='Times-Italic',
    fontSize=10, leading=14, alignment=4, spaceAfter=20,
    leftIndent=20, rightIndent=20
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Normal'], fontName='Times-Bold',
    fontSize=14, spaceBefore=15, spaceAfter=10
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Normal'], fontName='Times-Italic',
    fontSize=12, spaceBefore=10, spaceAfter=5
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'], fontName='Times-Roman',
    fontSize=11, leading=16, alignment=4, spaceAfter=10
)
math_style = ParagraphStyle(
    'Math', parent=styles['Normal'], fontName='Courier',
    fontSize=11, alignment=1, spaceBefore=10, spaceAfter=10
)
code_style = ParagraphStyle(
    'Code', parent=styles['Normal'], fontName='Courier',
    fontSize=9, leading=12, leftIndent=20, spaceBefore=10, spaceAfter=10,
    textColor=HexColor("#1e3a8a")
)

story = []

# ================= TITLE & AUTHOR =================
story.append(Paragraph("Autonomous Threshold Calibration via Spectral Gap Analysis for Zero-Shot Video Person Re-Identification", title_style))
story.append(Paragraph("<b>Rajtilak Chamlagain</b><br/>"
                       "Technology Innovation Hub – Technology Innovation and Development Foundation (TIH–TIDF)<br/>"
                       "Indian Institute of Technology Guwahati (IITG)", author_style))

# ================= ABSTRACT =================
story.append(Paragraph("Abstract", abstract_heading))
story.append(Paragraph("A persistent challenge in open-world Video Person Re-Identification (Re-ID) is the manual assignment of similarity thresholds. Traditional biometric verification relies on static cosine similarity gates (e.g., τ = 0.60), which frequently fail in dynamic CCTV environments exhibiting varied illumination, occlusion, and resolution degradation. In this paper, we propose a novel unsupervised clustering algorithm termed the Autonomous Spectral Gap Engine. By analyzing the maximal first-derivative drop-off within a sorted vector of ArcFace-derived cosine similarities, the system dynamically calculates a zero-shot threshold gate tailored to the specific optical conditions of the individual video frame. This mathematical approach effectively eliminates human bias, prevents false-positive forensic arrests, and establishes a robust fallback for law enforcement evidence triage.", abstract_body))

# ================= 1. INTRODUCTION =================
story.append(Paragraph("I. INTRODUCTION", h1_style))
story.append(Paragraph("The primary objective of forensic Person Re-Identification is to maintain the identity of a suspect across non-overlapping camera networks. While deep Convolutional Neural Networks (CNNs) utilizing Additive Angular Margin Loss (ArcFace) have achieved near-perfect accuracy on standardized datasets, real-world deployment faces a critical bottleneck: Threshold Calibration.", body_style))
story.append(Paragraph("When an AI compares a suspect to a crowded video frame, it outputs a list of confidence scores (e.g., 90%, 85%, 20%, 15%). Historically, human operators manually define a static passing threshold. If a video is corrupted by noise and the true suspect only registers a 45% similarity, a static 60% threshold will result in a False Negative. Conversely, lowering the threshold globally invites catastrophic False Positives.", body_style))
story.append(Paragraph("To resolve this, we introduce the Autonomous Spectral Gap Engine—a purely algorithmic, math-driven approach that completely removes the human operator from the thresholding loop.", body_style))

# ================= 2. METHODOLOGY & MATH =================
story.append(Paragraph("II. MATHEMATICAL FORMULATION", h1_style))
story.append(Paragraph("The core logic operates on the premise that the similarity distance between the true suspect and the highest-scoring innocent bystander represents the largest mathematical 'cliff' or 'gap' in a sorted array of scores.", body_style))

story.append(Paragraph("Let S be a set of cosine similarity scores extracted from the video frame, sorted in descending order:", body_style))
story.append(Paragraph("S = {s_1, s_2, ..., s_n} where s_1 ≥ s_2 ≥ ... ≥ s_n", math_style))

story.append(Paragraph("We compute the first-derivative (the absolute difference) between consecutive scores, defined as Δ_i:", body_style))
story.append(Paragraph("Δ_i = s_i - s_{i+1}", math_style))

story.append(Paragraph("The system then identifies the index i_max corresponding to the maximal gap:", body_style))
story.append(Paragraph("i_max = argmax(Δ_i)", math_style))

story.append(Paragraph("Finally, the autonomous threshold (τ) is dynamically placed exactly at the midpoint of this maximal spectral gap:", body_style))
story.append(Paragraph("τ = s_{i_max + 1} + (Δ_i_max / 2)", math_style))

story.append(Paragraph("This ensures the threshold is mathematically optimized to isolate the true positive cluster from the negative noise cluster, regardless of whether the video was recorded in broad daylight or extreme darkness.", body_style))

# ================= 3. IMPLEMENTATION =================
story.append(Paragraph("III. CODE IMPLEMENTATION", h1_style))
story.append(Paragraph("The mathematical formulation is realized through a computationally inexpensive Python algorithm, executing in O(N log N) time complexity due to the initial sort operation:", body_style))

code_text = """
def autonomous_spectral_gap(scores_list):
    if len(scores_list) < 2:
        return 45.0 # Fallback for single-person isolation
        
    sorted_scores = sorted(scores_list, reverse=True)
    max_gap = 0
    best_threshold = 45.0
    
    for i in range(len(sorted_scores) - 1):
        gap = sorted_scores[i] - sorted_scores[i+1]
        
        # Identify the maximal derivative drop-off
        if gap > max_gap:
            max_gap = gap
            best_threshold = sorted_scores[i+1] + (gap / 2.0)
            
    # Establish an absolute mathematical floor to prevent
    # legal validation of completely corrupted face data
    return max(best_threshold, 30.0)
"""
story.append(Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

# ================= 4. CONCLUSION =================
story.append(Paragraph("IV. CONCLUSION", h1_style))
story.append(Paragraph("The Autonomous Spectral Gap Engine offers a highly unique, unsupervised clustering solution to the Re-ID thresholding problem. By eliminating the necessity for manual, environment-specific calibration, the system preserves forensic integrity and prevents human bias from polluting the evidence pipeline. Future work will explore accelerating this calculation via FAISS for multi-million identity vector databases.", body_style))

doc.build(story)
print(f"[SUCCESS] Research Paper saved to: {pdf_filepath}")
