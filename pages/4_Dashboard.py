import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Safely Get Data
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 3. Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

water = round(w * 0.035, 1)
protein = int(w * 1.6)

if "Loss" in u_goal:
    cal, steps = int(bmr * 1.2) - 500, 10000
    ex_type, ex_time = "Cardio (HIIT/Running)", "45-60 Mins"
elif "Gain" in u_goal:
    cal, steps = int(bmr * 1.2) + 400, 5000
    ex_type, ex_time = "Strength Training", "45 Mins"
else:
    cal, steps = int(bmr * 1.2), 8000
    ex_type, ex_time = "Brisk Walk / Yoga", "30 Mins"

# 4. Dashboard UI
st.title("📊 Your Health Dashboard")

# Feature Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔥 Calories", f"{cal} kcal")
m2.metric("💧 Water", f"{water} L")
m3.metric("🍗 Protein", f"{protein} g")
m4.metric("👟 Steps", f"{steps:,}")

st.divider()

# Exercise Feature
st.subheader("🏋️ Activity Suggestion")
e1, e2 = st.columns(2)
e1.info(f"**Exercise:** {ex_type}")
e2.success(f"**Duration:** {ex_time} Daily")

st.divider()

# 5. AI Menu Generator
st.subheader(f"🍱 {u_cuisine} Menu Plan")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("AI is generating..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Optimized prompt to avoid server busy errors
                prompt = f"1-day {u_cuisine} menu for {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {cal} cal. Break into Breakfast, Lunch, Dinner."
                
                response = model.generate_content(
                    prompt, 
                    generation_config={"max_output_tokens": 500, "temperature": 0.7}
                )
                st.markdown(response.text)
                st.balloons()
            except Exception:
                st.error("🚨 AI Servers are busy. Please wait 10 seconds and try again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
