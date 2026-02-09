import streamlit as st
import numpy as np
import time
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

st.title("AI Fitness Trainer – Cloud Version")

exercise = st.selectbox(
    "Select Exercise",
    ["Squat", "Push-up", "Bicep Curl", "Plank", "Jumping Jack"]
)

counter = 0
stage = None
feedback = ""
start_time = time.time()

CAL = {
    "Squat": 0.32,
    "Push-up": 0.29,
    "Bicep Curl": 0.18,
    "Jumping Jack": 0.20,
    "Plank": 0.05
}

def calculate_angle(a, b, c):
    a=np.array(a); b=np.array(b); c=np.array(c)
    r=np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(r*180.0/np.pi)
    if angle>180: angle=360-angle
    return angle


class VideoProcessor(VideoProcessorBase):

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # HERE – later we connect browser AI model
        # For now basic counter simulation so app works

        global counter, feedback

        if exercise == "Plank":
            counter = int(time.time() - start_time)
            feedback = "Hold straight body"

        calories = round(counter * CAL.get(exercise,0.2),2)

        # Display overlay
        import cv2
        cv2.putText(img,f"{exercise}: {counter}",
            (20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(img,feedback,
            (20,80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,165,255),2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


st.write("Press START and allow camera permission")

webrtc_streamer(key="fitness", video_processor_factory=VideoProcessor)

st.write("🔥 Calories burned estimate:")
st.write(round(counter * CAL.get(exercise,0.2),2))