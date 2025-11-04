import streamlit as st
import os
from PIL import Image, ImageOps
from pathlib import Path

# --- Configuration ---
UPLOAD_PIC_DIR = "files/photos"
UPLOAD_VID_DIR = "files/videos"
ARCHIVE_DIR = "files/archive"
MAX_FILE_SIZE_MB = 1500
SUPPORTED_EXTENSIONS = ["png", "jpg", "jpeg", "heic", "mp4", 'm4v', 'avi', "mov", "webm"]
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.heic']

os.makedirs(UPLOAD_PIC_DIR, exist_ok=True)
os.makedirs(UPLOAD_VID_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

WEDDING_NAME = os.environ.get('WEDDING_NAME', '<unset WEDDING_NAME env>')

def save_uploaded_file(uploaded_file):
    # Correct rotation if a picture
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        file_path = os.path.join(UPLOAD_PIC_DIR, uploaded_file.name)
        image = Image.open(uploaded_file)
        corrected_image = ImageOps.exif_transpose(image)
        corrected_image.save(file_path)
    else:
        file_path = os.path.join(UPLOAD_VID_DIR, uploaded_file.name)
        with open (file_path, "wb") as v:
            v.write(uploaded_file.read())

    return file_path

st.html("""
<style>

[data-testid='stFileUploaderDropzoneInstructions'] > div > span:first-of-type {
  display: none;
}

[data-testid='stFileUploaderDropzoneInstructions'] > div::before {
  content: 'Click Browse to upload'
}
</style>
""")
st.title(f"{WEDDING_NAME} Wedding")
st.write("Upload your picture(s) here for the slideshow")

uploaded_files = st.file_uploader(
    label="Choose a photo file",
    label_visibility='collapsed',
    type=SUPPORTED_EXTENSIONS,
    accept_multiple_files=True
)

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # --- Verify extension (already handled by 'type' parameter but can be double-checked) ---
        file_extension = Path(uploaded_file.name).suffix[1:].lower()

        # --- Verify file size ---
        file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert bytes to MB

        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"Error: File size ({file_size_mb:.2f} MB) exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.")
        elif file_extension not in SUPPORTED_EXTENSIONS:
            st.error(f"Error: Unsupported file extension '.{file_extension}'. Please upload a PNG, JPG, or JPEG.")
        else:
            # --- Save the file to disk ---
            with st.spinner(f"Saving {uploaded_file.name}..."):
                saved_path = save_uploaded_file(uploaded_file)
                st.success("File uploaded successfully")

            # Optional: Display the uploaded image
            file_extension = Path(saved_path).suffix[1:].lower()
