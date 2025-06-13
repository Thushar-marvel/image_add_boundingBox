import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("Draw Normalized Bounding Box on Uploaded Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    h, w = image_np.shape[:2]

    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Enter normalized Bounding Box coordinates (between 0.0 and 1.0):")
    # Normalized coordinates input
    xmin = st.number_input("x_min (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    ymin = st.number_input("y_min (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    xmax = st.number_input("x_max (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
    ymax = st.number_input("y_max (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.9, step=0.01)

    if st.button("Draw Bounding Box"):
        image_with_bbox = image_np.copy()

        # Convert normalized to absolute pixel coordinates
        x1 = int(xmin * w)
        y1 = int(ymin * h)
        x2 = int(xmax * w)
        y2 = int(ymax * h)

        # Draw rectangle using OpenCV (color BGR)
        cv2.rectangle(
            image_with_bbox,
            (x1, y1),
            (x2, y2),
            color=(0, 255, 0),
            thickness=2,
        )
        st.image(image_with_bbox, caption="Image with Bounding Box", use_column_width=True)
