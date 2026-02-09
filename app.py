import streamlit as st
import mediapipe as mp
import numpy as np
import cv2
import time

st.set_page_config(page_title="AI Fitness Trainer", layout="centered")

st.title("🏋️ AI Fitness Trainer – Cloud Version")
st.write("Works on mobile & browser — no installation needed!")

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

exercise = st.selectbox(
    "Select Exercise",
    ["Squat", "Push-up", "Bicep Curl", "Plank", "Jumping Jack"]
)

reset = st.button("Reset Session")

CAL = {
    "Squat": 0.32,
    "Push-up": 0.29,
    "Bicep Curl": 0.18,
    "Jumping Jack": 0.20,
    "Plank": 0.05
}

if "counter" not in st.session_state:
    st.session_state.counter = 0
    st.session_state.stage = None
    st.session_state.start = time.time()

if reset:
    st.session_state.counter = 0
    st.session_state.stage = None
    st.session_state.start = time.time()
    st.success("Session Reset!")

# ===== ANGLE FUNCTION =====
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180:
        angle = 360-angle
    return angle


# ===== CAMERA INPUT (CLOUD SAFE) =====
img_file = st.camera_input("Take a photo for analysis")

if img_file is not None:

    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    feedback = "Get in position"

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        lm = results.pose_landmarks.landmark

        # ===== SQUAT =====
        if exercise == "Squat":
            hip = [lm[23].x, lm[23].y]
            knee = [lm[25].x, lm[25].y]
            ankle = [lm[27].x, lm[27].y]

            angle = calculate_angle(hip, knee, ankle)

            if angle > 160:
                st.session_state.stage = "UP"

            if angle < 95 and st.session_state.stage == "UP":
                st.session_state.stage = "DOWN"
                st.session_state.counter += 1
                feedback = "✅ Good Squat!"

            elif angle > 100 and angle < 140:
                feedback = "⬇ Go Lower"

        # ===== PUSH UP =====
        if exercise == "Push-up":
            shoulder = [lm[11].x, lm[11].y]
            elbow = [lm[13].x, lm[13].y]
            wrist = [lm[15].x, lm[15].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 165:
                st.session_state.stage = "UP"

            if angle < 70 and st.session_state.stage == "UP":
                st.session_state.stage = "DOWN"
                st.session_state.counter += 1
                feedback = "✅ Good Push-up!"

            elif angle > 80 and angle < 120:
                feedback = "⬇ Chest Lower"

        # ===== BICEP CURL =====
        if exercise == "Bicep Curl":
            shoulder = [lm[11].x, lm[11].y]
            elbow = [lm[13].x, lm[13].y]
            wrist = [lm[15].x, lm[15].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 155:
                st.session_state.stage = "DOWN"

            if angle < 35 and st.session_state.stage == "DOWN":
                st.session_state.stage = "UP"
                st.session_state.counter += 1
                feedback = "✅ Good Curl!"

        # ===== JUMPING JACK =====
        if exercise == "Jumping Jack":
            lw, rw = lm[15].y, lm[16].y
            la, ra = lm[27].x, lm[28].x

            hands_up = lw < 0.35 and rw < 0.35
            legs_apart = abs(la - ra) > 0.25

            if hands_up and legs_apart:
                st.session_state.stage = "OPEN"

            if (not hands_up) and (not legs_apart) and st.session_state.stage == "OPEN":
                st.session_state.stage = "CLOSE"
                st.session_state.counter += 1
                feedback = "✅ Good Jump!"

        # ===== PLANK =====
        if exercise == "Plank":
            st.session_state.counter = int(time.time() - st.session_state.start)
            feedback = "Hold Straight Body"

        calories = round(st.session_state.counter * CAL.get(exercise, 0.2), 2)

        st.image(frame, channels="BGR")

        st.subheader(f"🏆 Reps: {st.session_state.counter}")
        st.subheader(f"🔥 Calories: {calories}")
        st.info(feedback)

    else:
        st.warning("No body detected — adjust camera")

else:
    st.info("Open camera and take a photo to start")