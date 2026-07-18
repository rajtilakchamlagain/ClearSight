from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'ClearSight: Supervisor Meeting Talking Points', 0, 1, 'C')
        self.set_font('Arial', 'I', 11)
        self.cell(0, 8, 'A guide for explaining the architecture, failures, and engineering solutions.', 0, 1, 'C')
        self.set_line_width(0.5)
        self.line(10, 28, 200, 28)
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=11)

def add_section(title, content):
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102) # Dark blue
    pdf.cell(0, 10, title, 0, 1)
    
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, content)
    pdf.ln(5)

# --- SECTION 1 ---
sec1 = (
    "FaceNet is a facial recognition system developed by Google. Instead of just outputting 'Match' or 'No Match', "
    "it mathematically maps a face into a 512-dimensional space, creating a unique 'numerical fingerprint'.\n\n"
    "Why we used it: We used FaceNet running on the InceptionResnetV1 architecture because it supports 'Zero-Shot Learning'. "
    "This means we do NOT need to manually train a model on thousands of pictures of a target. We can just give it "
    "1 reference photo, extract the fingerprint, and instantly search for it in CCTV footage."
)
add_section("1. What is FaceNet (And Why We Used It)", sec1)

# --- SECTION 2 ---
sec2 = (
    "We designed a multi-stage pipeline because CCTV footage is usually blurry, badly lit, and angled.\n"
    "Step 1: MTCNN for Face Detection. We chose MTCNN over older models (like Haar Cascades) because MTCNN mathematically "
    "locates 5 facial landmarks (eyes, nose, mouth). We need these landmarks to fix tilted heads.\n"
    "Step 2: 2D Affine Transformation. Using the eyes, we mathematically rotate the face so it is perfectly straight.\n"
    "Step 3: CLAHE (Illumination Fix). We flatten harsh shadows and brighten dark spots.\n"
    "Step 4: FaceNet Vector Extraction. The perfect face is fed into FaceNet to extract the 512-D fingerprint."
)
add_section("2. What We Planned (The Core Architecture)", sec2)

# --- SECTION 3 ---
sec3 = (
    "During testing, we encountered three massive engineering failures:\n\n"
    "A. The 'Squashed Torso' Bug: When feeding the reference selfies to the AI, we forgot to crop the face first! "
    "The AI squashed the entire upper body and background into FaceNet. It was comparing a squashed torso to a CCTV face, resulting in terrible accuracy (38%).\n\n"
    "B. The 'Knee Match' Bug: MTCNN was set too sensitive. In a group photo, it hallucinated faces on random body parts (like knees and elbows).\n\n"
    "C. The 'Unnormalized Euclidean' Bug: We tried using Euclidean Distance (measuring physical distance between vectors), but "
    "FaceNet vectors are unnormalized. This caused the random knee vector to accidentally score better than an actual human face!"
)
add_section("3. What Failed During Testing", sec3)

# --- SECTION 4 ---
sec4 = (
    "We applied rigorous engineering solutions to fix the pipeline:\n\n"
    "Fix 1 (The Apples-to-Apples Fix): We built a universal 'get_perfect_face()' function. Now, the reference selfies go through "
    "the EXACT same MTCNN cropping and alignment process as the CCTV faces before FaceNet sees them.\n\n"
    "Fix 2 (Threshold Strictness): We increased MTCNN's confidence threshold to filter out false positives (knees/elbows).\n\n"
    "Fix 3 (Cosine Similarity): We switched from Euclidean Distance to Cosine Similarity. Cosine measures angles instead of physical size, "
    "making it immune to unnormalized vector explosions.\n\n"
    "Fix 4 (The Ultimate Upgrade - Multi-Anchor Ensembling): Instead of relying on 1 reference selfie (which suffers from lens distortion), "
    "we fused 3 different reference photos together into a single 'Master Super-Vector'. This made the AI incredibly robust to different facial expressions and angles."
)
add_section("4. How We Fixed It (The Engineering Solutions)", sec4)

output_path = r"C:\Users\rajti\Downloads\Projects\ACADEMIC INTERNSHIP\ClearSight_Project\data\Rajtilak_Meeting_Notes.pdf"
pdf.output(output_path)
print(f"Generated meeting notes at: {output_path}")
