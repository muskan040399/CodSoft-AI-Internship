import streamlit as st
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from PIL import Image
import cv2
import os
import urllib.request

# Page Configuration
st.set_page_config(
    page_title="FaceVision - AI Face Detection Studio",
    page_icon="👤",
    layout="centered"
)

st.title("👤 FaceVision: AI Face Detection")
st.markdown("""
Detect and localize human faces using Google's modern **MediaPipe** framework. 
Upload an image to run the high-performance face detection pipeline.
""")

# Automatically download the model file if it doesn't exist
MODEL_FILENAME = 'blaze_face_short_range.tflite'
MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite'

@st.cache_resource
def download_model():
    if not os.path.exists(MODEL_FILENAME):
        with st.spinner("Downloading AI model weights (first-time setup only)..."):
            urllib.request.urlretrieve(MODEL_URL, MODEL_FILENAME)
    return MODEL_FILENAME

model_path = download_model()

# Initialize the modern Face Detector safely
@st.cache_resource
def load_detector():
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceDetectorOptions(base_options=base_options)
    return vision.FaceDetector.create_from_options(options)

detector = load_detector()

# File Uploader
uploaded_file = st.file_uploader("Upload an image with faces...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    img_array = np.array(image)
    
    # Convert RGB to MediaPipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_array)
    
    # Run detection
    detection_result = detector.detect(mp_image)
    
    annotated_image = img_array.copy()
    face_count = len(detection_result.detections)
    
    # Draw bounding boxes manually using OpenCV
    for detection in detection_result.detections:
        bbox = detection.bounding_box
        start_point = (bbox.origin_x, bbox.origin_y)
        end_point = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
        
        # Draw rectangle (Green box)
        cv2.rectangle(annotated_image, start_point, end_point, (0, 255, 0), 3)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Detected Output")
        st.image(annotated_image, use_container_width=True)
        
    st.success(f"Successfully analyzed image! **{face_count} face(s) detected.**")
else:
    st.info("💡 **Tip:** Upload an image to test the AI face detection engine.")