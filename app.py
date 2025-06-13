import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("Draw Bounding Box on Uploaded Image")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Read image as array
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.write("Enter Bounding Box coordinates (xmin, ymin, xmax, ymax):")
    # Input for coordinates
    xmin = st.number_input("xmin", min_value=0, max_value=image_np.shape[1], value=0)
    ymin = st.number_input("ymin", min_value=0, max_value=image_np.shape[0], value=0)
    xmax = st.number_input("xmax", min_value=0, max_value=image_np.shape[1], value=image_np.shape[1]//2)
    ymax = st.number_input("ymax", min_value=0, max_value=image_np.shape[0], value=image_np.shape[0]//2)
    
    if st.button("Draw Bounding Box"):
        image_with_bbox = image_np.copy()
        # Draw rectangle using OpenCV (color BGR)
        cv2.rectangle(
            image_with_bbox,
            (int(xmin), int(ymin)),
            (int(xmax), int(ymax)),
            color=(0, 255, 0),
            thickness=2,
        )
        st.image(image_with_bbox, caption="Image with Bounding Box", use_column_width=True)
