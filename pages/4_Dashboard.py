import streamlit as st
import google.generativeai as genai
import time

# 1. Page Config
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Get data from Step 1 (session_state)
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 3. CALCULATIONS ---
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water & Protein
water = round(w * 0.035, 1)
protein = int(w * 1.6)

# Goal-based logic for Steps and Exercise
if "Loss" in u_goal:
    cal, steps = int(bmr * 1.2) - 500, 10000
    ex_type, ex_time = "Cardio (HIIT/Running)", "45-60 Mins"
elif "Gain" in u_goal:
    cal, steps = int(bmr * 1.2) + 400, 5000
    ex_type, ex_time = "Strength Training", "45 Mins"
else:
    cal, steps = int(bmr * 1.2), 8000
    ex_type, ex_time = "Brisk Walk / Yoga", "30 Mins"

# --- 4. UI DISPLAY ---
st.title("📊 Your Health Dashboard")

# Metric Bar
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔥 Calories", f"{cal} kcal")
m2.metric("💧 Water", f"{water} L")
m3.metric("🍗 Protein", f"{protein} g")
m4.metric("👟 Steps", f"{steps:,}")

st.divider()

# Exercise Feature
st.subheader("🏋️ Exercise Suggestion")
e1, e2 = st.columns(2)
e1.info(f"**Activity:** {ex_type}")
e2.success(f"**Duration:** {ex_time} Daily")

st.divider()

# --- 5. THE AI GENERATOR (FIXED FOR BUSY SERVERS) ---
st.subheader(f"🍱 {u_cuisine} Food Menu")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing! Check Streamlit Secrets.")
    else:
        with st.spinner("AI is generating your plan..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                # We use 1.5-flash as it is the most stable under high traffic
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Optimized prompt: Short and direct to reduce server load
                prompt = f"1-day {u_cuisine} menu for {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {cal} kcal. Format: Breakfast, Lunch, Dinner."
                
                # CRITICAL FIX: Limit the output size so the server doesn't time out
                response = model.generate_content(
                    prompt, 
                    generation_config={"max_output_tokens": 450, "temperature": 0.7}
                )
                
                st.markdown(response.text)
                st.balloons()
            except Exception:
                # If it still fails, wait 3 seconds and try one last time automatically
                st.warning("Server is busy. Retrying automatically...")
                time.sleep(3)
                try:
                    response
