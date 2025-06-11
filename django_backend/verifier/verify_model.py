import os
import mimetypes
from PIL import Image
from PIL.ExifTags import TAGS
import PyPDF2
import exifread

def identify_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type == 'application/pdf':
            return 'pdf'
        elif mime_type.startswith('image/jpeg'):
            return 'jpeg'
        elif mime_type.startswith('image/png'):
            return 'png'
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in ['.pdf']:
        return 'pdf'
    elif ext in ['.jpg', '.jpeg']:
        return 'jpeg'
    elif ext == '.png':
        return 'png'
    return 'unknown'

def extract_pdf_metadata(file_path):
    print("\n[PDF Metadata]")
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        info = reader.metadata
        for key, value in info.items():
            print(f"{key}: {value}")

def extract_image_metadata_pillow(file_path):
    print("\n[Image Metadata using Pillow]")
    img = Image.open(file_path)
    exif_data = img._getexif()
    if exif_data:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag}: {value}")
    else:
        print("No EXIF metadata found using Pillow.")

def extract_image_metadata_exifread(file_path):
    print("\n[Image Metadata using ExifRead]")
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag in tags:
            print(f"{tag}: {tags[tag]}")

def extract_metadata(file_path):
    file_type = identify_file_type(file_path)
    print(f"Detected file type: {file_type.upper()}")
    if file_type == 'pdf':
        extract_pdf_metadata(file_path)
    elif file_type in ['jpeg', 'png']:
        extract_image_metadata_pillow(file_path)
        extract_image_metadata_exifread(file_path)
    else:
        print("Unsupported or unknown file type.")

# Example usage
file_path = "example_file_here"  # Replace with your actual file path
extract_metadata(file_path)
