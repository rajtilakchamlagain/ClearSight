from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        # Arial bold 16
        self.set_font('Arial', 'B', 16)
        # Title
        self.cell(0, 10, 'Project Summary Report', 0, 1, 'C')
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        # Line break
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=11)

def add_inline_field(title, content):
    pdf.set_font("Arial", 'B', 12)
    # Get width of title string
    title_w = pdf.get_string_width(title) + 2
    pdf.cell(title_w, 8, title, 0, 0)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, content, 0, 1)

def add_section(title, content):
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, title, 0, 1)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, content)
    pdf.ln(4)

add_inline_field('Group Members:', 'Rajtilak Chamlagain (Solo)')
add_inline_field('Supervisor Name:', 'Dr. Mahapara Khursid')
add_inline_field('Project Title:', 'ClearSight: Deep Learning-Based Target Detection & Tracking System')
pdf.ln(4)

abstract = (
    "This project focuses on developing an advanced computer vision pipeline for real-time target "
    "detection and tracking in low-quality CCTV environments. Utilizing MTCNN for robust facial landmark "
    "detection and DeepSORT for continuous object tracking, the system overcomes traditional challenges "
    "like poor illumination and motion blur. A mathematical preprocessing engine comprising Affine "
    "Transformations for 2D facial alignment and CLAHE (Contrast Limited Adaptive Histogram Equalization) "
    "is implemented to normalize environmental distortions before feature extraction via FaceNet. "
    "The primary objective is to accurately detect and persistently track individuals of interest across frames, "
    "providing a highly scalable security monitoring tool without the need for model retraining."
)
add_section("Abstract:", abstract)

details = (
    "- Software: Python, PyTorch (CUDA-accelerated), OpenCV, Flask (for Web UI backend).\n"
    "- Core Models: MTCNN (Target Detection), InceptionResnetV1 / FaceNet (Feature Extraction), "
    "DeepSORT (Video Tracking).\n"
    "- Processing Pipeline: 2D Face Alignment (Affine Transforms) and Illumination Normalization (CLAHE) "
    "to optimize features for zero-shot recognition."
)
add_section("Details of the Software/Hardware to be implemented:", details)

components = (
    "- Hardware Compute: A machine equipped with an NVIDIA GPU (supporting CUDA) for "
    "real-time tensor acceleration and neural network inference.\n"
    "- Video Input: Standard IP Camera or pre-recorded CCTV footage for pipeline processing."
)
add_section("Components required (if any):", components)

# Save to data folder
output_path = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project\data\Rajtilak_Project_Summary_V3.pdf"
pdf.output(output_path)
print(f"PDF successfully generated at: {output_path}")
