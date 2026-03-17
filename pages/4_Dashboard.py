import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. FETCH DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. CALCULATE BMI & VITALS
bmi = round(w / ((h/100)**2), 1)
status = "Healthy"
if bmi < 18.5: status = "Underweight"
elif bmi >= 25 and bmi < 30: status = "Overweight"
elif bmi >= 30: status = "Obese"

# 3. INTERACTIVE INTENSITY & STEP LOGIC
st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic Mapping for Steps and Multipliers
if intensity == "Rest":
    mult, water_add, prot_rate, steps = 1.2, 0.0, 1.2, 4000
elif intensity == "Light":
    mult, water_add, prot_rate, steps = 1.375, 0.5, 1.4, 7000
elif intensity == "Moderate":
    mult, water_add, prot_rate, steps = 1.55, 1.0, 1.8, 10000
else: # Heavy
    mult, water_add, prot_rate, steps = 1.725, 1.5, 2.2, 15000

# Final Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal_target = int(bmr * mult) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot_target = int(w * prot_rate)
water_target = round((w * 0.035) + water_add, 1)

# 4. DISPLAY DASHBOARD
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal_target} kcal")
c2.metric("🍗 Protein", f"{prot_target} g")
c3.metric("💧 Water", f"{water_target} L")
c4.metric("👟 Steps", f"{steps:,}")

st.info(f"**BMI:** {bmi} ({status}) | **Today's Goal:** {intensity} Activity")

# 5. FIXED AI COACH (Workout + Diet)
st.divider()
if st.button("🚀 Generate My AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("AI Coach is building your plan..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Single-line prompt to prevent parsing errors
                prompt = f"Diet and Workout Coach for {g}, {a}yo, {w}kg. BMI {bmi}, Goal {goal}, {intensity} intensity. Suggest 45m workout and {cuisine} menu for {cal_target}cal and {prot_target}g protein."
                
                res = model.generate_content(prompt, generation_config={"temperature": 0.2, "max_output_tokens": 600})
                st.markdown(res.text)
                st.balloons()
            except:
                st.error("AI Busy. Please wait 10s and try again.")
