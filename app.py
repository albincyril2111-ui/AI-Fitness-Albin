import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import numpy as np
import av
import time

st.title("AI Fitness Trainer – Cloud Version")

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()

exercise = st.selectbox(
    "Select Exercise",
    ["Squat", "Push-up", "Bicep Curl", "Plank", "Jumping Jack"]
)

counter = 0
stage = None
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


class AITrainer(VideoProcessorBase):

    def recv(self, frame):
        global counter, stage

        img = frame.to_ndarray(format="bgr24")
        rgb = img[:, :, ::-1]

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
                    stage="UP"

                elif angle<95 and stage=="UP":
                    stage="DOWN"
                    counter+=1

            if exercise=="Plank":
                counter=int(time.time()-start_time)

            cv2.putText(
                img,
                f"{exercise}: {counter}",
                (20,40),
                0,1,(0,255,0),2
            )

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="fitness",
    video_processor_factory=AITrainer
)

st.write("Reps / Seconds:", counter)
st.write("Calories:", round(counter*CAL.get(exercise,0.2),2))