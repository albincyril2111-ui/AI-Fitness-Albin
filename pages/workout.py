import streamlit as st
import mediapipe as mp
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("Workout Mode – Cloud")

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

exercise = st.selectbox(
    "Select Exercise",
    ["Squat", "Push-up", "Bicep Curl", "Jumping Jack"]
)

counter = 0
stage = None

def calculate_angle(a, b, c):
    a=np.array(a); b=np.array(b); c=np.array(c)
    r=np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(r*180.0/np.pi)
    if angle>180: angle=360-angle
    return angle


class AITrainer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = img[:,:,::-1]
        results = pose.process(rgb)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        return img


webrtc_streamer(
    key="workout",
    video_transformer_factory=AITrainer,
    media_stream_constraints={"video": True, "audio": False},
)