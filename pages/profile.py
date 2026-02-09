import streamlit as st
from theme import load_theme
from database import init_profile, save_profile, get_profile

st.markdown(load_theme(), unsafe_allow_html=True)

st.title("User Profile & BMI")

init_profile()

profile = get_profile()

name = st.text_input("Name", profile[1] if profile else "")
age = st.number_input("Age", 10, 80, profile[2] if profile else 20)

height = st.number_input(
    "Height (cm)", 100, 220, int(profile[3]) if profile else 170
)

weight = st.number_input(
    "Weight (kg)", 30, 200, int(profile[4]) if profile else 70
)

goal = st.selectbox(
    "Goal",
    ["Weight Loss", "Muscle Gain", "Fitness", "Endurance"],
    index=0 if not profile else
    ["Weight Loss","Muscle Gain","Fitness","Endurance"].index(profile[5])
)

# ----- BMI -----
bmi = round(weight / ((height/100)**2), 2)

st.markdown(f"""
<div class='card'>
Your BMI: <b>{bmi}</b>
</div>
""", unsafe_allow_html=True)

if st.button("Save Profile"):
    save_profile(name, age, height, weight, goal, bmi)
    st.success("Profile Saved!")