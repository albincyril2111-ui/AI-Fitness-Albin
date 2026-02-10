import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import time

st.title("AI Fitness Trainer – Cloud Safe Version")

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
        img = frame.to_ndarray(format="bgr24")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        movement = np.mean(blur)

        # SIMPLE REP LOGIC (Cloud Compatible)
        if movement > 60 and self.stage == "UP":
            self.stage = "DOWN"

        if movement < 40 and self.stage == "DOWN":
            self.stage = "UP"
            self.counter += 1

        cv2.putText(img, f"Reps: {self.counter}",
            (20,40), cv2.FONT_HERSHEY_SIMPLEX,
            1,(0,255,0),2)

        calories = round(self.counter * CAL[exercise],2)

        cv2.putText(img, f"Calories: {calories}",
            (20,80), cv2.FONT_HERSHEY_SIMPLEX,
            1,(0,255,255),2)

        return img


webrtc_streamer(
    key="fitness",
    video_transformer_factory=Trainer,
    media_stream_constraints={"video": True, "audio": False},
)

st.info("Allow camera permission in browser ↑")