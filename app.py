import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.title("AI Fitness Trainer – Cloud Safe")

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()

CAL = {
    "Squat": 0.32,
    "Push-up": 0.29,
    "Bicep Curl": 0.18,
    "Jumping Jack": 0.20,
    "Plank": 0.05
}

exercise = st.selectbox(
    "Select Exercise",
    list(CAL.keys())
)

def calculate_angle(a,b,c):
    a=np.array(a); b=np.array(b); c=np.array(c)
    r=np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(r*180/np.pi)
    if angle>180: angle=360-angle
    return angle


class AIProcessor(VideoProcessorBase):

    counter = 0
    stage = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            lm = results.pose_landmarks.landmark

            if exercise=="Squat":
                hip=[lm[23].x,lm[23].y]
                knee=[lm[25].x,lm[25].y]
                ankle=[lm[27].x,lm[27].y]

                angle=calculate_angle(hip,knee,ankle)

                if angle>165:
                    self.stage="UP"

                if angle<95 and self.stage=="UP":
                    self.stage="DOWN"
                    self.counter+=1

            cv2.putText(img,f"Reps: {self.counter}",
                (20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        return frame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="fitness",
    video_processor_factory=AIProcessor
)