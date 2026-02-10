import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np

st.title("AI Fitness Trainer – Web Only Version")

exercise = st.selectbox(
    "Select Exercise",
    ["Squat", "Push-up", "Bicep Curl"]
)

CAL = {
    "Squat": 0.32,
    "Push-up": 0.29,
    "Bicep Curl": 0.18
}

class Trainer(VideoTransformerBase):
    def __init__(self):
        self.counter = 0
        self.stage = "UP"

    def transform(self, frame):
        img = frame.to_ndarray(format="rgb24")

        movement = np.mean(img)

        if movement > 140 and self.stage == "UP":
            self.stage = "DOWN"

        if movement < 100 and self.stage == "DOWN":
            self.stage = "UP"
            self.counter += 1

        # Draw overlay using numpy only
        h, w, _ = img.shape
        img[10:60, 10:300] = [0, 0, 0]

        calories = round(self.counter * CAL[exercise], 2)

        return img


webrtc_streamer(
    key="fitness",
    video_transformer_factory=Trainer,
    media_stream_constraints={"video": True, "audio": False},
)

st.write("Reps counted using motion AI")
st.info("Allow camera permission ↑")