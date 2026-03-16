import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- 1. GET DATA FROM YOUR FRONT PAGE ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 2. CALCULATIONS (Updates as you change weight/age) ---
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water & Protein math
water = round(w * 0.035, 1)
protein = int(w * 1.6)

# Goal-based Exercise and Steps
if "Loss" in u_goal:
    cal, steps = int(bmr * 1.2) - 500, 10000
    ex_type, ex_time = "Cardio (HIIT/Running)", "45-60 Mins"
elif "Gain" in u_goal:
    cal, steps = int(bmr * 1.2) + 400, 5000
    ex_type, ex_time = "Strength Training", "45 Mins"
else:
    cal, steps = int(bmr * 1.2), 8000
    ex_type, ex_time = "Brisk Walk / Yoga", "30 Mins"

# --- 3. UI DISPLAY ---
st.title("🛡️ Cura AI Dashboard")

# Feature Row: Calories, Water, Protein, Steps
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("💧 Water", f"{water} L")
c3.metric("🍗 Protein", f"{protein} g")
c4.metric("👟 Steps", f"{steps:,}")

st.divider()

# Feature: Exercise Suggestion with Time
st.subheader("🏋️ Exercise Recommendation")
e1, e2 = st.columns(2)
e1.info(f"**Activity:** {ex_type}")
e2.success(f"**Duration:** {ex_time} Daily")

st.divider()

# --- 4. THE AI MENU (PROPER CODE) ---
st.subheader(f"🍱 {u_cuisine} Food Menu")

if st.button("✨ Generate My Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing! Check Streamlit Secrets.")
    else:
        with st.spinner("AI is generating your plan..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Concise prompt to prevent "Overload" errors
                prompt = f"Create a 1-day {u_cuisine} diet for a {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {cal} cal. Include Breakfast, Lunch, Dinner."
                
                # Generation config to keep it light
                response = model.generate_content(
                    prompt, 
                    generation_config={"max_output_tokens": 500, "temperature": 0.7}
                )
                
                st.markdown(response.text)
                st.balloons()
            except Exception:
                st.error("🚨 AI Servers are busy. Wait 10 seconds and try again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
