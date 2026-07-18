from fpdf import FPDF
import os

class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.set_text_color(0, 51, 102) # Dark Blue
        self.cell(0, 12, 'ClearSight Project', 0, 1, 'C')
        
        self.set_font('Arial', 'I', 14)
        self.set_text_color(100, 100, 100) # Gray
        self.cell(0, 8, 'Comprehensive Engineering & Progress Report (V1)', 0, 1, 'C')
        
        self.set_line_width(0.5)
        self.set_draw_color(0, 51, 102)
        self.line(10, 32, 200, 32)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(230, 240, 255) # Light Blue background
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, f' {title}', 0, 1, 'L', fill=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, body)
        self.ln(6)
        
    def add_subheading(self, text, color=(0, 0, 0)):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*color)
        self.cell(0, 8, text, 0, 1)
        
    def add_bullet(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, f"  * {text}")

pdf = ReportPDF()
pdf.add_page()

# --- INTRO ---
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Author: Rajtilak Chamlagain | Supervisor: Dr. Mahapara Khursid', 0, 1)
pdf.ln(5)
intro = (
    "This document serves as a living record of the ClearSight AI-Powered Target Detection "
    "and Tracking System. It details every architectural decision, engineering failure, and "
    "mathematical solution implemented up to the current phase."
)
pdf.chapter_body(intro)

# --- PHASE 1 ---
pdf.chapter_title("Phase 1: Environment & Hardware Acceleration")
pdf.add_subheading("The Core Idea:")
pdf.chapter_body("To process CCTV frames in real-time, we needed to bypass the CPU and run all tensor calculations directly on an NVIDIA GPU using CUDA architecture.")
pdf.add_subheading("What Failed (The CUDA Mismatch):", color=(180, 0, 0))
pdf.chapter_body("Our initial PyTorch installation did not align with the system's CUDA 11.8 drivers. This caused tensor mismatch errors where the Neural Network was loaded onto the GPU, but the image tensors were stuck on the CPU. They could not communicate.")
pdf.add_subheading("How We Fixed It:", color=(0, 128, 0))
pdf.chapter_body("We wiped the environment and forced a strict installation of torch-2.7.1+cu118. We implemented strict .to(device) routing in the code to guarantee data locality.")

# --- PHASE 2 & 3 ---
pdf.chapter_title("Phase 2 & 3: MTCNN Detection & 2D Alignment")
pdf.add_subheading("The Core Idea:")
pdf.chapter_body("Instead of using basic Haar Cascades, we utilized MTCNN (Multi-task Cascaded Convolutional Networks) to extract 5 precise facial landmarks (eyes, nose, mouth). We then used the distance between the left and right eyes to mathematically calculate the tilt angle of the head and apply a 2D Affine Transformation to straighten it.")
pdf.add_subheading("What Failed (The Knee Hallucination):", color=(180, 0, 0))
pdf.chapter_body("MTCNN's default confidence thresholds were too low [0.4, 0.5, 0.5]. During testing on a group photo, the AI hallucinated a face on a random patch of skin (a knee/elbow) in the background.")
pdf.add_subheading("How We Fixed It:", color=(0, 128, 0))
pdf.chapter_body("We tightened the steps_threshold to [0.7, 0.8, 0.8]. This completely eliminated false positives while maintaining target detection.")

# --- PHASE 4 ---
pdf.chapter_title("Phase 4: Illumination Normalization")
pdf.add_subheading("The Core Idea:")
pdf.chapter_body("CCTV footage suffers from harsh shadows. We converted the RGB image to LAB color space and isolated the L-channel (Lightness). We applied CLAHE (Contrast Limited Adaptive Histogram Equalization) to flatten the shadows and brighten dark spots without washing out the colors, simulating perfect studio lighting.")

# --- PHASE 5 & 6 ---
pdf.chapter_title("Phase 5 & 6: FaceNet Extraction & Math Failures")
pdf.add_subheading("The Core Idea:")
pdf.chapter_body("We fed the aligned, perfectly lit faces into the InceptionResnetV1 (FaceNet) model to extract a 512-Dimensional mathematical fingerprint. We then used vector distance formulas to compare the CCTV face to the reference photo.")
pdf.add_subheading("What Failed (The Squashed Torso Bug):", color=(180, 0, 0))
pdf.chapter_body("We accidentally fed the raw, uncropped reference selfies into FaceNet. The AI squashed the user's entire upper body and background into a 160x160 square, completely destroying the mathematical signature. The match accuracy plummeted to 38%.")
pdf.add_subheading("What Failed (The Euclidean Math Explosion):", color=(180, 0, 0))
pdf.chapter_body("We attempted to use Euclidean Distance on unnormalized FaceNet vectors. Because the vectors had varying magnitudes, random noise (like the knee patch) accidentally scored a shorter distance than actual complex human faces.")
pdf.add_subheading("How We Fixed It:", color=(0, 128, 0))
pdf.chapter_body("1. We built a universal get_perfect_face() function. This guarantees that BOTH the reference selfies and the CCTV footage go through the exact same MTCNN cropping and CLAHE alignment pipeline before FaceNet sees them (Apples-to-Apples comparison).\n2. We abandoned Euclidean Distance and switched to Cosine Similarity, which purely measures the angle between vectors and naturally ignores vector magnitude.")

# --- PHASE 7.5 ---
pdf.chapter_title("Phase 7.5: The Accuracy Boosters")
pdf.add_subheading("The Core Idea:")
pdf.chapter_body("A single reference selfie is highly vulnerable to wide-angle lens distortion and expression changes (e.g., smiling vs neutral).")
pdf.add_subheading("The Engineering Solution (Multi-Anchor Ensembling):", color=(0, 128, 0))
pdf.chapter_body("Instead of relying on 1 photo, we prompted the system to ingest 3 distinct photos of the target. We fed all three into FaceNet and mathematically averaged their 512-D vectors together. This created a highly robust 'Master Super-Vector' that possesses a 3D understanding of the target's facial structure, drastically increasing zero-shot accuracy in the wild.")

output_path = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project\data\ClearSight_Comprehensive_Report_V1.pdf"
pdf.output(output_path)
print(f"Report generated successfully at: {output_path}")
