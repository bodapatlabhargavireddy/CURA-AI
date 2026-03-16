import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- 1. GET USER DATA ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 2. CALCULATIONS ---
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
water = round(w * 0.035, 1)
protein = int(w * 1.6)

if "Loss" in u_goal:
    cal, steps = int(bmr * 1.2) - 500, 10000
    ex_type, ex_time = "Cardio (Running/Cycling)", "45-60 Mins"
elif "Gain" in u_goal:
    cal, steps = int(bmr * 1.2) + 400, 5000
    ex_type, ex_time = "Strength Training", "45 Mins"
else:
    cal, steps = int(bmr * 1.2), 8000
    ex_type, ex_time = "Brisk Walk/Yoga", "30 Mins"

# --- 3. UI DISPLAY ---
st.title("📊 Your Health Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Calories", f"{cal} kcal")
col2.metric("💧 Water", f"{water} L")
col3.metric("🍗 Protein", f"{protein} g")
col4.metric("👟 Steps", f"{steps:,}")

st.divider()

# Exercise Feature
st.subheader("🏋️ Activity Suggestion")
e1, e2 = st.columns(2)
e1.info(f"**Exercise:** {ex_type}")
e2.success(f"**Duration:** {ex_time} Daily")

st.divider()

# --- 4. THE "NO-FAIL" AI GENERATOR ---
st.subheader(f"🍱 {u_cuisine} Menu Plan")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        # Configuration
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        prompt = f"Diet plan for {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {cal} cal. Exercise: {ex_type}."
        
        success = False
        # Try 3 times automatically
        for attempt in range(3):
            try:
                with st.spinner(f"Connecting to AI (Attempt {attempt+1}/3)..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    success = True
                    break # Stop trying if it works!
            except Exception:
                time.sleep(3) # Wait 3 seconds before trying again
        
        if not success:
            st.error("📢 Still Busy. Tip: Use a Mobile Hotspot for faster connection!")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
