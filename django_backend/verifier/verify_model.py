import os
import mimetypes
from PIL import Image, ImageChops, ImageEnhance
import exifread
import pytesseract
import requests
import re

# ---------------- STEP 1: File Type ----------------
def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    ext = os.path.splitext(file_path)[-1].lower()
    if 'pdf' in mime_type or ext == '.pdf':
        return 'pdf'
    elif 'jpeg' in mime_type or ext in ['.jpg', '.jpeg']:
        return 'jpeg'
    elif 'png' in mime_type or ext == '.png':
        return 'png'
    return 'unknown'

# ---------------- STEP 2: Metadata ----------------
def extract_metadata(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            metadata = {tag: str(tags[tag]) for tag in tags}
            return metadata
    except:
        return {}

# ---------------- STEP 3: ELA ----------------
def ela_analysis(image_path):
    try:
        original = Image.open(image_path).convert("RGB")
        resaved = "resaved.jpg"
        original.save(resaved, "JPEG", quality=90)
        resaved_image = Image.open(resaved)
        ela_image = ImageChops.difference(original, resaved_image)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        return max_diff
    except:
        return 0

# ---------------- STEP 4: OCR ----------------
def extract_text(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except:
        return ""

# ---------------- STEP 5: Identify ID Type ----------------
def identify_id_type(text):
    if re.search(r'\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b', text):
        return 'aadhar'
    elif re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', text):
        return 'pan'
    return 'unknown'

# ---------------- STEP 6: Dummy API Calls ----------------
def verify_aadhar(data):
    # Simulated API
    expected_name = "Aarthi"
    score = 100 if expected_name.lower() in data.lower() else 60
    return {"name": expected_name, "verified": True, "match_score": score}

def verify_pan(data):
    # Simulated API
    expected_pan = "ABCDE1234F"
    found = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', data)
    score = 100 if found and found.group() == expected_pan else 50
    return {"pan": expected_pan, "verified": True, "match_score": score}

# ---------------- STEP 7: Final Fraud Probability ----------------
def calculate_fraud_rate(meta, ela_score, api_result):
    fraud_score = 0
    if not meta:
        fraud_score += 20
    if ela_score > 50:
        fraud_score += 40
    if api_result['match_score'] < 80:
        fraud_score += 30
    return min(fraud_score, 100)

# ---------------- Main Orchestrator ----------------
def run_verification(file_path):
    print("File Path:", file_path)

    ftype = detect_file_type(file_path)
    print("Detected File Type:", ftype.upper())

    meta = extract_metadata(file_path)
    print(f"Metadata found: {len(meta)} tags")

    ela_score = ela_analysis(file_path) if ftype == 'jpeg' else 0
    print(f"Edit Likelihood Score (ELA): {ela_score}")

    text = extract_text(file_path)
    print("Extracted Text Preview:\n", text[:200])

    id_type = identify_id_type(text)
    print("Detected ID Type:", id_type.upper())

    if id_type == 'aadhar':
        api_result = verify_aadhar(text)
    elif id_type == 'pan':
        api_result = verify_pan(text)
    else:
        api_result = {'match_score': 30}

    fraud_probability = calculate_fraud_rate(meta, ela_score, api_result)
    print(f"\nEstimated Fraud Probability: {fraud_probability:.1f}%")

# ---------------- Entry Point ----------------
if __name__ == "__main__":
    file_path = "D:\SEM 6\CyberSec\Wireshark_Assignment_Aarthi.pdf"
    run_verification(file_path)
