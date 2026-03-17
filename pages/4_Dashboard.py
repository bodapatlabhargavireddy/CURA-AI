import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. DATA RECOVERY
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. LOCAL SCIENCE CALCULATIONS
bmi = round(w / ((h/100)**2), 1)
status = "Healthy"
if bmi < 18.5: status = "Underweight"
elif bmi >= 25 and bmi < 30: status = "Overweight"
elif bmi >= 30: status = "Obese"

# 3. INTERACTIVE INTENSITY
st.title("🛡️ Cura AI: Total Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Step & Logic Mapping
if intensity == "Rest":
    m, wa, p, steps = 1.2, 0.0, 1.2, 4000
elif intensity == "Light":
    m, wa, p, steps = 1.375, 0.5, 1.4, 7000
elif intensity == "Moderate":
    m, wa, p, steps = 1.55, 1.0, 1.8, 10000
else:
    m, wa, p, steps = 1.725, 1.5, 2.2, 15000

# Math Engine
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * m) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * p)
water = round((w * 0.035) + wa, 1)

# 4. DISPLAY DASHBOARD
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚖️ BMI", f"{bmi} ({status})")
c2.metric("🔥 Calories", f"{cal} kcal")
c3.metric("🍗 Protein", f"{prot} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal for {intensity} Day:** {steps:,} steps")
st.divider()

# 5. AI COACH (Workout + Diet)
if st.button("🚀 Generate AI Workout & Meal Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Add API Key to Secrets!")
    else:
        with st.spinner("AI Coach is preparing your plan..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Extremely clean prompt to avoid any parsing issues
                prompt = f"Act as fitness coach. User: {g}, {a}yo, {w}kg, BMI {bmi}. Intensity: {intensity}. Goal: {goal}. Cuisine: {cuisine}. Targets: {cal}kcal, {prot}g protein. Suggest a 45min workout and a 1-day meal plan."
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.balloons()
            except:
                st.error("AI Busy. The metrics above are still 100% accurate for your profile!")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
