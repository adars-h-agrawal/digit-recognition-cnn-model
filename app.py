import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load trained model (.keras format)
model = load_model("model.keras")

st.title("🖌️ Handwritten Digit Recognition")
st.write("Draw a digit (0–9) below and let the model predict!")

# Create a drawable canvas
canvas_result = st_canvas(
    fill_color="white",
    stroke_width=15,
    stroke_color="black",
    background_color="white",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)

# When something is drawn
if canvas_result.image_data is not None:
    img = canvas_result.image_data.astype("uint8")

    # Convert RGBA -> grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

    # Resize to 28x28 for MNIST
    resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)

    # Invert colors (white background, black digit)
    processed = 255 - resized

    # Normalize and reshape
    processed = processed / 255.0
    processed = processed.reshape(1, 28, 28, 1)

    # Predict
    prediction = model.predict(processed)
    digit = np.argmax(prediction)

    st.write(f"### Predicted Digit: **{digit}**")
