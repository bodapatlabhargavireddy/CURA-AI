import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. FETCH DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. ADVANCED MEASUREMENTS
bmi = round(w / ((h/100)**2), 1)

# Estimate Body Fat % (Standard BMI-based formula for adults)
if g == "Male":
    body_fat = round((1.20 * bmi) + (0.23 * a) - 16.2, 1)
else:
    body_fat = round((1.20 * bmi) + (0.23 * a) - 5.4, 1)

# BMI Category
if bmi < 18.5: status = "Underweight"
elif 18.5 <= bmi < 25: status = "Healthy"
elif 25 <= bmi < 30: status = "Overweight"
else: status = "Obese"

# 3. UI - INTENSITY SELECTION
st.title("🛡️ Cura AI: Clinical Dashboard")
st.subheader("Today's Vitals & Activity")

col_a, col_b = st.columns(2)
with col_a:
    ex_intensity = st.select_slider(
        "Exercise Intensity:",
        options=["Rest", "Light", "Moderate", "Heavy"]
    )
with col_b:
    st.info(f"**BMI:** {bmi} ({status}) | **Est. Body Fat:** {body_fat}%")

# 4. THE INTERCONNECTED LOGIC ENGINE
# Base Calories (Mifflin-St Jeor)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Adjustments based on BMI & Body Fat
# If BMI is 'Obese', we slightly increase water but keep protein moderate.
# If Body Fat is low, we increase protein to protect muscle.
if body_fat < 15 and g == "Male" or body_fat < 22 and g == "Female":
    protein_base = 2.2 # High protein for lean muscle
else:
    protein_base = 1.6 # Standard protein

# Multipliers based on intensity
intensity_map = {
    "Rest": {"cal": 1.2, "water": 0.0, "steps": 4000},
    "Light": {"cal": 1.375, "water": 0.5, "steps": 7000},
    "Moderate": {"cal": 1.55, "water": 1.0, "steps": 10000},
    "Heavy": {"cal": 1.725, "water": 1.5, "steps": 15000}
}

data = intensity_map[ex_intensity]

# Final Targets
cal_target = int(bmr * data["cal"])
if "Loss" in u_goal: cal_target -= 500
if "Gain" in u_goal: cal_target += 500

protein_target = int(w * protein_base)
water_target = round((w * 0.035) + data["water"], 1)
step_target = data["steps"]

# 5. DISPLAY RESULTS
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal_target} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water_target} L")
c4.metric("👟 Steps", f"{step_target:,}")

# 6. AI AGENT
st.subheader(f"🍱 {u_cuisine} Meal Plan (AI Optimized)")

if st.button("✨ Generate Plan"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (f"User: {g}, {a}yo, {w}kg. BMI: {bmi} ({status}), Body Fat: {body_fat}%. "
                  f"Activity: {ex_intensity}. Goal: {u_goal}. Cuisine: {u_cuisine}. "
                  f"Target: {cal_target}kcal, {protein_target}g protein. "
                  f"Provide a 1-day menu.")
        
        with st.spinner("AI analyzing body composition..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    except:
        st.error("AI servers busy. Try again in 10s.")
