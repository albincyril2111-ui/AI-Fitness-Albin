import streamlit as st
from theme import load_theme

st.markdown(load_theme(), unsafe_allow_html=True)

st.title("About Project")

st.markdown("""
<div class='card'>
AI Fitness Trainer  
- MediaPipe Pose  
- Python & Streamlit  
- Computer Vision  
- Final Year Project
</div>
""", unsafe_allow_html=True)