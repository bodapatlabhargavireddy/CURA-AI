import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. RETRIEVE DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. INSTANT SCIENCE ENGINE
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

# Intensity Logic
intensity = st.select_slider("Activity Level Today:", options=["Rest", "Light", "Moderate", "Heavy"])
i_map = {"Rest": 1.2, "Light": 1.375, "Moderate": 1.55, "Heavy": 1.725}

# Basic Math
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * i_map[intensity]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * 1.8)
fat = int((cal * 0.25) / 9)
water = round(w * 0.035, 1)

# 3. DISPLAY VITALS
st.title("🛡️ Cura AI Dashboard")
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal}")
c2.metric("🍗 Protein", f"{prot}g")
c3.metric("🥑 Fat", f"{fat}g")
c4.metric("💧 Water", f"{water}L")

st.info(f"📊 **BMI:** {bmi} ({status}) | **Goal:** {goal}")
st.divider()

# 4. THE AI PLANNER (Meal & Exercise)
if st.button("🚀 Generate AI Meal & Exercise Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key!")
    else:
        with st.spinner("AI is crafting your plan..."):
            try:
                # Setup AI
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # SHORT PROMPT = FAST RESPONSE
                prompt = (f"As a fitness coach, provide a 1-day {cuisine} meal plan "
                         f"and a workout for a {w}kg {g} with BMI {bmi}. "
                         f"Goal: {goal}, Intensity: {intensity}. "
                         f"Target: {cal}kcal, {prot}g Protein, {fat}g Fat.")
                
                # Optimized for maximum speed
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.balloons()
                else:
                    st.warning("AI Busy. Wait 5 seconds and click again.")
            except Exception:
                st.error("API Limit reached. Wait 10 seconds and try one last time.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
