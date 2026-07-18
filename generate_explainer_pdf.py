from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'FaceNet Explainer Guide', 0, 1, 'C')
        self.set_font('Arial', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Simple Analogies & Architecture for Pen & Paper Explanations', 0, 1, 'C')
        self.set_draw_color(0, 51, 102)
        self.line(10, 28, 200, 28)
        self.ln(10)

    def add_section(self, title, text):
        self.set_font("Arial", 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, 0, 1)
        
        self.set_font("Arial", '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(5)

pdf = PDF()
pdf.add_page()

s1 = (
    "InceptionResnetV1 is a massive artificial brain made of two brilliant ideas combined:\n\n"
    "1. Inception: Normal networks look at an image one way. 'Inception' modules look at the image at multiple "
    "zoom levels simultaneously (e.g., looking at the whole face, and zooming in on just the pupil of the eye) "
    "to catch big and small details.\n"
    "2. ResNet (Residual Network): When a network is very deep, it tends to 'forget' information from early layers. "
    "ResNet introduces 'shortcuts' that let the original image data jump forward, ensuring no details are lost.\n\n"
    "How to draw it: Draw a straight line with a few boxes (normal network). Then draw a curved line that skips over "
    "the boxes (the ResNet shortcut)."
)
pdf.add_section("1. What is the InceptionResnetV1 Architecture?", s1)

s2 = (
    "Traditional AI (like an old dog) requires you to feed it 10,000 photos of yourself and 'train' it for days just "
    "to recognize you.\n\n"
    "Zero-Shot Learning means the AI is already a trained detective. It understands what a 'human face' is fundamentally. "
    "You do not need to train it on your specific face. You just hand the detective 1 photo of you (the reference photo), "
    "and it instantly knows how to find you in a crowd without any retraining."
)
pdf.add_section("2. What is Zero-Shot Learning?", s2)

s3 = (
    "Imagine you are standing in the center of a room, pointing two laser pointers at the wall.\n"
    "- Euclidean Distance measures the physical distance (in inches) between the two red dots on the wall.\n"
    "- Cosine Similarity measures the ANGLE between your two arms.\n\n"
    "Why does this matter? If the CCTV camera is blurry, the 'length' of the face vector shrinks (the red dot moves "
    "closer). Euclidean distance would fail because the physical distance changed. But Cosine Similarity ignores the "
    "length entirely; it only checks if the two vectors are pointing in the exact same direction."
)
pdf.add_section("3. What is Cosine Similarity?", s3)

s4 = (
    "Every time FaceNet looks at a photo, it outputs a list of exactly 512 numbers (the numerical fingerprint).\n\n"
    "If we feed it 3 selfies, we get three lists of 512 numbers. We literally use basic math to add the lists together "
    "and divide by 3 (we calculate the Mean Average).\n"
    "If Selfie 1 says your jawline thickness is 5, Selfie 2 says 6, and Selfie 3 says 7, the Master Vector averages it "
    "to a 6. This mathematically smooths out any weird lens distortions or bad lighting from a single bad selfie."
)
pdf.add_section("4. How did we fuse 3 photos into a Master Super-Vector?", s4)

s5 = (
    "Draw this exact flow on the whiteboard to explain the Pipeline:\n\n"
    "[CCTV Camera Frame] --> [MTCNN (Detects 5 Landmarks)] --> [2D Affine Alignment (Straightens Head Tilt)] --> "
    "[CLAHE (Removes Shadows)] --> [FaceNet Engine (Extracts Target Fingerprint)]\n\n"
    "Then, from the bottom:\n"
    "[3x Reference Selfies] --> [Mathematical Average] --> [Master Super-Vector]\n\n"
    "Finally, draw an arrow from [Target Fingerprint] and [Master Super-Vector] pointing into "
    "[Cosine Similarity (Matches Angle)]."
)
pdf.add_section("5. The Architecture Block Diagram", s5)

output = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project\data\FaceNet_Explainer_Guide.pdf"
pdf.output(output)
print(f"Generated explainer pdf at: {output}")
