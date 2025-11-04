import streamlit as st
import glob
import os
import time
from datetime import datetime as dt
from datetime import timedelta as td
from PIL import Image

# Set the page title and layout
st.set_page_config(page_title="Photo Slideshow", layout="wide")

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

def initialize_session_state(image_paths):
    """Initialize session state for the slideshow."""
    if 'current_image_index' not in st.session_state:
        st.session_state.current_image_index = 0
    if 'image_paths' not in st.session_state:
        st.session_state.image_paths = image_paths

def next_image():
    """Go to the next image in the slideshow."""
    if st.session_state.image_paths:
        st.session_state.current_image_index = (
            st.session_state.current_image_index + 1
        ) % len(st.session_state.image_paths)

def prev_image():
    """Go to the previous image in the slideshow."""
    if st.session_state.image_paths:
        st.session_state.current_image_index = (
            st.session_state.current_image_index - 1
        ) % len(st.session_state.image_paths)

# --- Main App Logic ---

# Get image file paths and update session state
image_paths = get_image_files(IMAGES_DIR)
initialize_session_state(image_paths)
# Check if there are any images to display
if not st.session_state.image_paths:
    st.warning(f"No image files found in the '{IMAGES_DIR}' folder. Please add some images.")
else:
    # Display the current image
    try:
        current_image_path = st.session_state.image_paths[st.session_state.current_image_index]
        image = Image.open(current_image_path)
        st.image(image, use_container_width="auto") # width='stretch'
    except:
        st.error(f"Image not found... rerunning")
        # Reset to avoid further errors if a file was deleted
        st.session_state.image_paths = get_image_files(IMAGES_DIR)
        st.rerun()

    # Slideshow controls
    row = st.container(border = False)
    with row:
        col1, col2 = st.columns(2, width='stretch')
        with col1:
            st.button("Previous", on_click=prev_image, width='stretch')
        with col2:
            st.button("Next", on_click=next_image, width='stretch')

    if 'last_run_time' not in st.session_state:
        st.session_state.last_run_time = dt.now()

    timer_interval = td(seconds=5)
    refresh_interval = td(seconds=60)
    # Check if the timer has expired
    if dt.now() - st.session_state.last_run_time >= timer_interval:
        next_image()
        st.session_state.last_run_time = dt.now()  # Reset the timer
        image_paths = get_image_files(IMAGES_DIR)
        st.session_state.image_paths = image_paths
        st.rerun()  # Force a re-run to update the display
    else:
        # Display a message or other content while waiting for the timer
        st.write("Waiting for timer...")
        time.sleep(1)  # Add a small delay to prevent excessive re-runs
        st.rerun()  # Force re-run to keep checking the time
time.sleep(1)
st.session_state.image_paths = get_image_files(IMAGES_DIR)
st.rerun()
