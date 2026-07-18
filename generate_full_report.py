import os
from fpdf import FPDF

# Clean up old/redundant PDFs
base_path = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project\data"
old_files = [
    "Rajtilak_Project_Summary.pdf",
    "Rajtilak_Project_Summary_V2.pdf",
    "ClearSight_Comprehensive_Report_V1.pdf"
]

for f in old_files:
    path = os.path.join(base_path, f)
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Could not delete {f}: {e}")

# Generate New Fixed PDF
class DetailedPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'ClearSight: Deep Learning-Based', 0, 1, 'C')
        self.cell(0, 10, 'Target Detection & Tracking System', 0, 1, 'C')
        
        self.set_font('Arial', 'I', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Full Detailed Project Report (From Inception to Current Phase)', 0, 1, 'C')
        
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.8)
        self.line(10, 38, 200, 38)
        
        # CRITICAL FIX: Ensures text never overlaps the header on Page 2!
        self.set_y(45)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(220, 235, 255) # Light blue
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, f' {title}', 0, 1, 'L', fill=True)
        self.ln(2)

    def add_subheading(self, text, color=(0, 0, 0)):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*color)
        self.cell(0, 8, text, 0, 1)
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, body)
        self.ln(6)

pdf = DetailedPDF()
# CRITICAL FIX: Automatically creates new pages cleanly without cutting off text
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Author: Rajtilak Chamlagain | Supervisor: Dr. Mahapara Khursid', 0, 1)
pdf.ln(5)

# --- 1. Abstract & Introduction ---
pdf.chapter_title("1. Abstract & Introduction")
intro = (
    "The ClearSight project was conceptualized to solve the problem of identifying and tracking targets in "
    "low-quality CCTV environments. Traditional models fail when faced with poor lighting, motion blur, and "
    "off-angle faces. Our solution implements a multi-stage Deep Learning pipeline that mathematically "
    "normalizes environmental distortions before utilizing a zero-shot learning approach for target re-identification."
)
pdf.chapter_body(intro)

# --- 2. Phase 1 ---
pdf.chapter_title("2. Phase 1: Environment & Hardware Acceleration")
pdf.add_subheading("The Plan:")
pdf.chapter_body("To achieve real-time video processing, the entire pipeline was engineered to run on NVIDIA CUDA architecture, bypassing the CPU.")
pdf.add_subheading("What Went Wrong (The Tensor Mismatch Bug):", color=(180, 0, 0))
pdf.chapter_body("Our initial PyTorch installation did not align with the system's CUDA 11.8 drivers. This caused tensor mismatch errors where the Neural Network was loaded onto the GPU, but the image tensors were stuck on the CPU.")
pdf.add_subheading("How We Fixed It:", color=(0, 128, 0))
pdf.chapter_body("We enforced a strict re-installation of torch-2.7.1+cu118 and implemented strict .to(device) routing across the entire codebase to guarantee memory locality.")

# --- 3. Phase 2 & 3 ---
pdf.chapter_title("3. Phase 2 & 3: MTCNN Detection & 2D Alignment")
pdf.add_subheading("The Plan:")
pdf.chapter_body("We utilized MTCNN (Multi-task Cascaded Convolutional Networks) to extract 5 precise facial landmarks. We used the mathematical distance between the eyes to calculate the head's tilt angle and applied a 2D Affine Transformation to straighten the face.")
pdf.add_subheading("What Went Wrong (The Knee Hallucination):", color=(180, 0, 0))
pdf.chapter_body("MTCNN was initially too sensitive (thresholds of [0.4, 0.5, 0.5]). During group photo testing, the AI hallucinated a face on a random patch of skin (a knee) in the background.")
pdf.add_subheading("How We Fixed It:", color=(0, 128, 0))
pdf.chapter_body("We tightened the steps_threshold to [0.7, 0.8, 0.8]. This completely eliminated false positives while keeping actual targets.")

# --- 4. Phase 4 ---
pdf.chapter_title("4. Phase 4: Illumination Normalization")
pdf.add_subheading("The Plan & Execution:")
pdf.chapter_body("CCTV footage suffers from harsh shadows. We converted the RGB image to LAB color space and isolated the L-channel (Lightness). We applied CLAHE (Contrast Limited Adaptive Histogram Equalization) to flatten the shadows and brighten dark spots without washing out the colors, simulating studio lighting.")

# --- 5. Phase 5 & 6 ---
pdf.chapter_title("5. Phase 5 & 6: FaceNet Extraction & Math Failures")
pdf.add_subheading("The Plan (InceptionResnetV1 & FaceNet):")
pdf.chapter_body("We fed the aligned faces into an InceptionResnetV1 neural network backbone that was pre-trained using the FaceNet methodology. FaceNet maps the face into a 512-Dimensional mathematical space, outputting a numerical fingerprint.")
pdf.add_subheading("What Went Wrong (The Squashed Torso Bug):", color=(180, 0, 0))
pdf.chapter_body("We accidentally fed raw, uncropped reference selfies into FaceNet. The AI compressed the user's entire upper body and background into a 160x160 square, destroying the mathematical signature. Accuracy fell to 38%.")
pdf.add_subheading("What Went Wrong (The Euclidean Explosion):", color=(180, 0, 0))
pdf.chapter_body("We attempted to use Euclidean Distance on unnormalized FaceNet vectors. This caused random background noise to score mathematically closer than actual complex human faces.")
pdf.add_subheading("How We Fixed It:", color=(0, 128, 0))
pdf.chapter_body("1. We built a universal get_perfect_face() function so BOTH the reference selfies and the CCTV footage go through the exact same MTCNN cropping and alignment pipeline.\n2. We switched to Cosine Similarity, which purely measures the angle between vectors and is immune to magnitude explosions.")

# --- 6. Phase 7.5 ---
pdf.chapter_title("6. Phase 7.5: The Accuracy Boosters")
pdf.add_subheading("The Plan:")
pdf.chapter_body("A single reference selfie is highly vulnerable to lens distortion and facial expression changes.")
pdf.add_subheading("The Solution (Multi-Anchor Ensembling):", color=(0, 128, 0))
pdf.chapter_body("Instead of relying on 1 photo, we prompted the system to ingest 3 distinct photos of the target. We fed all three into FaceNet and mathematically averaged their 512-D vectors together. This created a highly robust 'Master Super-Vector', drastically increasing real-world detection accuracy.")

output_path = os.path.join(base_path, "ClearSight_Full_Detailed_Report_Final.pdf")
pdf.output(output_path)
print(f"Report generated successfully at: {output_path}")
