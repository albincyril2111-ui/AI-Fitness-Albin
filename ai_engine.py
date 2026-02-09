import cv2
import mediapipe as mp
import numpy as np
import time

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# Better stability settings
pose = mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
    model_complexity=1
)

CAL = {
    "Squat": 0.32,
    "Push-up": 0.29,
    "Bicep Curl": 0.18,
    "Jumping Jack": 0.20,
    "Plank": 0.05
}

last_rep_time = 0
MIN_REP_GAP = 1.2   # seconds between reps


def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)

    r = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(r * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle


def allow_rep():
    global last_rep_time
    if time.time() - last_rep_time > MIN_REP_GAP:
        last_rep_time = time.time()
        return True
    return False


def process_frame(frame, exercise, counter, stage, start_time):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    feedback = ""

    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        lm = results.pose_landmarks.landmark

        # ===== SQUAT =====
        if exercise == "Squat":
            hip   = [lm[23].x, lm[23].y]
            knee  = [lm[25].x, lm[25].y]
            ankle = [lm[27].x, lm[27].y]

            angle = calculate_angle(hip, knee, ankle)

            if angle > 165:
                stage = "UP"

            elif angle < 95 and stage == "UP":
                # depth validation
                if knee[1] > hip[1] and allow_rep():
                    counter += 1
                    stage = "DOWN"
                    feedback = "Good Squat"
                else:
                    feedback = "Go deeper"

        # ===== PUSH UP =====
        if exercise == "Push-up":
            shoulder = [lm[11].x, lm[11].y]
            elbow    = [lm[13].x, lm[13].y]
            wrist    = [lm[15].x, lm[15].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            # elbow flare check
            if abs(shoulder[0] - elbow[0]) > 0.18:
                feedback = "Elbows too wide"

            elif angle > 165:
                stage = "UP"

            elif angle < 65 and stage == "UP" and allow_rep():
                counter += 1
                stage = "DOWN"
                feedback = "Good Push-up"

        # ===== BICEP CURL =====
        if exercise == "Bicep Curl":
            shoulder = [lm[11].x, lm[11].y]
            elbow    = [lm[13].x, lm[13].y]
            wrist    = [lm[15].x, lm[15].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            # anti swing
            if abs(shoulder[1] - elbow[1]) > 0.10:
                feedback = "Keep elbow fixed"

            elif angle > 155:
                stage = "DOWN"

            elif angle < 35 and stage == "DOWN" and allow_rep():
                counter += 1
                stage = "UP"
                feedback = "Good Curl"

        # ===== JUMPING JACK =====
        if exercise == "Jumping Jack":
            lw, rw = lm[15].y, lm[16].y
            la, ra = lm[27].x, lm[28].x

            hands_up   = lw < 0.30 and rw < 0.30
            legs_apart = abs(la - ra) > 0.28

            if hands_up and legs_apart:
                stage = "OPEN"

            elif (not hands_up) and (not legs_apart) and stage == "OPEN":
                if allow_rep():
                    counter += 1
                    stage = "CLOSE"
                    feedback = "Good Jump"

        # ===== PLANK =====
        if exercise == "Plank":
            counter = int(time.time() - start_time)
            feedback = "Hold straight body"

    calories = round(counter * CAL.get(exercise, 0.2), 2)
    elapsed  = int(time.time() - start_time)

    return frame, counter, stage, feedback, calories, elapsed