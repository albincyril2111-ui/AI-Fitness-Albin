import streamlit as st
import pandas as pd
from theme import load_theme
from database import get_history

st.markdown(load_theme(), unsafe_allow_html=True)

st.title("Progress Dashboard 📊")

data = get_history()

# ---- No data case ----
if not data:
    st.info("No workout history yet. Complete a session first!")
    st.stop()

# ---- Convert to DataFrame ----
df = pd.DataFrame(
    data,
    columns=["ID", "Exercise", "Count", "Calories", "Duration", "Date"]
)

# ========== SUMMARY CARDS ==========
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sessions", len(df))

with col2:
    st.metric("Total Calories", round(df["Calories"].sum(), 2))

with col3:
    st.metric("Total Reps/Secs", df["Count"].sum())

st.markdown("</div>", unsafe_allow_html=True)


# ========== EXERCISE WISE GRAPH ==========
st.subheader("Reps by Exercise")

exercise_chart = df.groupby("Exercise")["Count"].sum()
st.bar_chart(exercise_chart)


# ========== CALORIES GRAPH ==========
st.subheader("Calories Burned")

cal_chart = df.groupby("Exercise")["Calories"].sum()
st.bar_chart(cal_chart)


# ========== BEST PERFORMANCE ==========
best = df.loc[df["Count"].idxmax()]

st.markdown(f"""
<div class='card'>
🏆 Best Performance<br>
Exercise: {best['Exercise']}<br>
Count: {best['Count']}<br>
Calories: {best['Calories']}<br>
Date: {best['Date']}
</div>
""", unsafe_allow_html=True)


# ========== FULL HISTORY ==========
st.subheader("Workout History")

st.dataframe(
    df[["Date", "Exercise", "Count", "Calories", "Duration"]],
    use_container_width=True
)