import streamlit as st
import numpy as np
import cv2
from PIL import Image
import json
import matplotlib.pyplot as plt

st.title("Draw MULTIPLE Normalized Bounding Boxes on Uploaded Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    h, w = image_np.shape[:2]

    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.write("""
    Enter a list of **normalized bounding boxes** as JSON.  
    Each box: `[x_min, y_min, x_max, y_max]` (values 0.0–1.0).  
    Example for two boxes:  
    ```
    [
      [0.1, 0.1, 0.4, 0.4],
      [0.5, 0.5, 0.9, 0.9]
    ]
    ```
    """)

    boxes_json = st.text_area("Bounding boxes (JSON)", value='[\n  [0.1, 0.1, 0.4, 0.4],\n  [0.5, 0.5, 0.9, 0.9]\n]')
    
    if st.button("Draw Bounding Boxes"):
        try:
            boxes = json.loads(boxes_json)
            if not isinstance(boxes, list) or not all(isinstance(b, list) and len(b) == 4 for b in boxes):
                st.error("Invalid format. Please provide a list of [x_min, y_min, x_max, y_max] boxes.")
            else:
                image_with_boxes = image_np.copy()
                # Use matplotlib's tab10 colormap for distinct colors
                colormap = plt.get_cmap('tab10')
                for i, (xmin, ymin, xmax, ymax) in enumerate(boxes):
                    x1 = int(xmin * w)
                    y1 = int(ymin * h)
                    x2 = int(xmax * w)
                    y2 = int(ymax * h)
                    rgb = np.array(colormap(i % 10)[:3]) * 0.4  # 0.4 = 40%, you can tweak this
                    color = tuple(int(255*c) for c in rgb[::-1])
                    
                    cv2.rectangle(
                        image_with_boxes,
                        (x1, y1),
                        (x2, y2),
                        color=color,
                        thickness=2,
                    )
                st.image(image_with_boxes, caption="Image with Bounding Boxes", use_container_width=True)
        except Exception as e:
            st.error(f"Error parsing bounding boxes: {e}")
