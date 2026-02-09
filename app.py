import streamlit as st
import mediapipe as mp
import numpy as np
import cv2
import time
import threading
import pyttsx3

# ---------- Smart Voice ----------
def speak_async(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 155)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()


st.title("AI Fitness Trainer – Smart Coach")

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()

exercise = st.selectbox(
    "Select Exercise",
    ["Squat", "Push-up", "Bicep Curl", "Plank", "Jumping Jack"]
)

reset = st.button("Reset Session")

FRAME_WINDOW = st.image([])

counter = 0
stage = None
feedback = ""
last_voice = ""
rep_voice_gate = 0
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

def smart_speak(msg, force=False):
    global last_voice, rep_voice_gate

    if msg == last_voice and not force:
        return

    if "Good" in msg:
        rep_voice_gate += 1
        if rep_voice_gate % 3 != 0:
            return

    speak_async(msg)
    last_voice = msg


if reset:
    counter=0; start_time=time.time(); feedback="Session Reset!"
    smart_speak("Session reset", True)


# ===============================
# ✅ STREAMLIT CAMERA INPUT
# ===============================

camera = st.camera_input("Use your Camera")

if camera is not None:

    file_bytes = np.asarray(bytearray(camera.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    frame=cv2.flip(frame,1)
    frame=cv2.resize(frame,(640,480))

    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=pose.process(rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS)

        lm=results.pose_landmarks.landmark

        # ========== SQUAT ==========
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
                feedback="Good squat"
                smart_speak(feedback)

        # ========== PUSH UP ==========
        if exercise=="Push-up":
            shoulder=[lm[11].x,lm[11].y]
            elbow=[lm[13].x,lm[13].y]
            wrist=[lm[15].x,lm[15].y]

            angle=calculate_angle(shoulder,elbow,wrist)

            if angle>165:
                stage="UP"

            elif angle<65 and stage=="UP":
                stage="DOWN"
                counter+=1
                feedback="Good push-up"
                smart_speak(feedback)

        # ========== BICEP CURL ==========
        if exercise=="Bicep Curl":
            shoulder=[lm[11].x,lm[11].y]
            elbow=[lm[13].x,lm[13].y]
            wrist=[lm[15].x,lm[15].y]

            angle=calculate_angle(shoulder,elbow,wrist)

            if angle>155:
                stage="DOWN"

            elif angle<35 and stage=="DOWN":
                stage="UP"
                counter+=1
                feedback="Good curl"
                smart_speak(feedback)

        # ========== JUMPING JACK ==========
        if exercise=="Jumping Jack":
            lw, rw = lm[15].y, lm[16].y
            la, ra = lm[27].x, lm[28].x

            hands_up = lw < 0.35 and rw < 0.35
            legs_apart = abs(la-ra) > 0.25

            if hands_up and legs_apart:
                stage="OPEN"

            if (not hands_up) and (not legs_apart) and stage=="OPEN":
                stage="CLOSE"
                counter+=1
                feedback="Good jump"
                smart_speak(feedback)

        # ========== PLANK ==========
        if exercise=="Plank":
            counter=int(time.time()-start_time)
            feedback="Hold straight body"

        calories=round(counter*CAL.get(exercise,0.2),2)

        cv2.putText(frame,f"{exercise}: {counter}",
            (20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(frame,feedback,
            (20,80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,165,255),2)

    FRAME_WINDOW.image(frame)