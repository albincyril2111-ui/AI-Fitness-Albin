import streamlit as st
from theme import load_theme

st.markdown(load_theme(), unsafe_allow_html=True)

st.title("AI PERSONAL FITNESS TRAINER")

st.markdown("""
<div class='card'>
🔥 Welcome to your AI powered gym coach  
✔ Real-time exercise tracking  
✔ Form correction  
✔ Calories estimation  
✔ Progress analytics  
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Workout"):
        st.switch_page("pages/Workout.py")

with col2:
    if st.button("View Progress"):
        st.switch_page("pages/Progress.py")

st.markdown("""
<div class='card'>
💡 Train smarter, not harder.  
Your AI coach watches every rep!
</div>
""", unsafe_allow_html=True)