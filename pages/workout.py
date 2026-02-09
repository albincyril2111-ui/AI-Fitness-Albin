import streamlit as st
import cv2
import numpy as np
import time

from theme import load_theme
from ai_engine import process_frame
from database import save_session, init_db, get_profile

init_db()

st.markdown(load_theme(), unsafe_allow_html=True)

st.title("Workout Zone")

# ----- PROFILE BAR -----
profile = get_profile()

if profile:
    st.markdown(f"""
    <div class='card'>
    👤 <b>{profile[1]}</b> |
    Goal: <b>{profile[5]}</b> |
    BMI: <b>{profile[6]}</b>
    </div>
    """, unsafe_allow_html=True)

exercise = st.selectbox(
    "Choose Exercise",
    ["Squat", "Push-up", "Bicep Curl", "Jumping Jack", "Plank"]
)

# ---- MOBILE CAMERA OPTION ----
phone_cam = st.camera_input("Use Phone Camera (Optional)")

run = st.checkbox("Start Training")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

counter = 0
stage = None
start_time = 0

if run and start_time == 0:
    start_time = time.time()


# ========== MAIN LOOP ==========
while run:

    # phone camera priority
    if phone_cam:
        file_bytes = np.asarray(bytearray(phone_cam.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)
    else:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera Error")
            break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    frame, counter, stage, feedback, calories, elapsed = process_frame(
        frame, exercise, counter, stage, start_time
    )

    # ---- Goal Tip ----
    tip = ""
    if profile:
        goal = profile[5]
        if goal == "Weight Loss":
            tip = "Tip: Focus on Jumping Jacks & Squats"
        elif goal == "Muscle Gain":
            tip = "Tip: Push-ups & Bicep Curls"
        elif goal == "Endurance":
            tip = "Tip: Longer Plank holds"
        else:
            tip = "Tip: Mixed routine"

    cv2.putText(frame, f"{exercise}: {counter}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.putText(frame, f"Calories: {calories}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 0, 0), 2)

    cv2.putText(frame, feedback,
                (20, 120), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 165, 255), 2)

    if tip:
        cv2.putText(frame, tip,
                    (20, 160), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 0), 2)

    FRAME_WINDOW.image(frame)

# ===== AFTER SESSION =====
if not run and counter > 0:

    save_session(exercise, counter, calories, elapsed)

    st.markdown(f"""
    <div class='card'>
    🏁 Session Saved!<br>
    Exercise: {exercise}<br>
    Reps/Seconds: {counter}<br>
    Calories: {calories}<br>
    Duration: {elapsed}s
    </div>
    """, unsafe_allow_html=True)

cap.release()