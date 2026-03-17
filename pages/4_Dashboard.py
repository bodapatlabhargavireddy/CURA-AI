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

# 2. THE SCIENCE ENGINE (Local & Instant)
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Total Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic for dynamic scaling
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "s": 4000, "work": "Active Recovery / Stretching"},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.4, "s": 7000, "work": "Brisk Walking or Yoga"},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "s": 10000, "work": "Weight Training or Steady Cardio"},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "s": 15000, "work": "HIIT or Heavy Strength Circuit"}
}
lvl = i_map[intensity]

# Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
water = round((w * 0.035) + lvl["w"], 1)

# 3. DISPLAY DASHBOARD
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚖️ BMI", f"{bmi} ({status})")
c2.metric("🔥 Calories", f"{cal} kcal")
c3.metric("🍗 Protein", f"{prot} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Steps:** {lvl['s']:,} | 🏋️ **Workout:** {lvl['work']}")

# 4. INSTANT LOCAL PLAN (The "Another Way")
st.divider()
st.subheader("📋 Your Personalized Plan")

# This part shows up instantly without AI
col_left, col_right = st.columns(2)
with col_left:
    st.write("### 🥗 Recommended Meals")
    st.write(f"- **Breakfast:** High Protein {cuisine} bowl (~{int(cal*0.25)} kcal)")
    st.write(f"- **Lunch:** Balanced {cuisine} platter with greens (~{int(cal*0.4)} kcal)")
    st.write(f"- **Dinner:** Light {cuisine} protein-focused meal (~{int(cal*0.35)} kcal)")

with col_right:
    st.write("### 🏃 Exercise Details")
    st.write(f"- **Intensity:** {intensity}")
    st.write(f"- **Focus:** {lvl['work']}")
    st.write(f"- **Target Steps:** {lvl['s']:,}")

# 5. OPTIONAL AI UPGRADE
st.divider()
if st.button("✨ Enhance Plan with AI (Gemini)"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"1-day {cuisine} menu for {w}kg {g}, BMI {bmi}, Intensity {intensity}. Goal {goal}. {cal}kcal, {prot}g protein."
        with st.spinner("AI is thinking..."):
            res = model.generate_content(prompt)
            st.markdown(res.text)
    except:
        st.error("AI Busy. Using the local scientific plan above.")
