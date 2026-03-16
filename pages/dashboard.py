import streamlit as st

def calculate_metrics():
    # Access shared state from main.py
    w, h, a, g = st.session_state.weight, st.session_state.height, st.session_state.age, st.session_state.gender
    goal, meds = st.session_state.goal, st.session_state.meds
    
    s = 5 if g == "Male" else -161
    bmr = (10 * w) + (6.25 * h) - (5 * a) + s
    tdee = bmr * 1.3 
    if goal == "Weight Loss": tdee -= 500
    elif goal == "Weight Gain": tdee += 400
    
    # Calculation Logic
    st.title("📊 Your Health Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Target Calories", f"{int(tdee)} kcal")
    c2.metric("Protein Goal", f"{int(w * 1.6)}g")
    c3.metric("Water Intake", f"{round(w * 0.035, 1)} L")

calculate_metrics()
