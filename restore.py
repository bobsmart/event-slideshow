import streamlit as st
import glob
import os
import shutil
import pandas as pd
from PIL import Image

from photo import ARCHIVE_DIR
from photo import UPLOAD_PIC_DIR

# Set the page title and layout
st.set_page_config(page_title="Manage", layout="wide")

# --- Configuration ---
# Folder where your images are located
IMAGES_DIR = "files/photos"
# Supported image file extensions
IMAGE_EXTENSIONS = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.heic']

# --- Functions ---
def get_image_files(directory):
    """Recursively get a sorted list of image file paths from a directory."""
    image_paths = []
    # Use glob to find all files matching the supported extensions
    for ext in IMAGE_EXTENSIONS:
        image_paths.extend(glob.glob(os.path.join(directory, ext)))
    # Sort the files by their name for a consistent display order
    return sorted(image_paths)

def delete_image(img):
    # file_path = os.path.join(IMAGES_DIR, img.name)
    shutil.move(img, UPLOAD_PIC_DIR)

# --- Main App Logic ---

# Get image file paths and update session state
image_paths = get_image_files(ARCHIVE_DIR)
selected_photos = []
for pic in image_paths:
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.checkbox(pic, key=pic):
            selected_photos.append(pic)
    with col2:
        image = Image.open(pic)
        st.image(image, width=100)

        # Button to move selected photos
if st.button("Move Selected Photos"):
    if selected_photos:
        for photo_to_move in selected_photos:
            delete_image(photo_to_move)

    st.rerun()
