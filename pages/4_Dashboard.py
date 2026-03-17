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

# 2. THE SCIENCE ENGINE (BMI & Body Fat)
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Total Performance Coach")
intensity = st.select_slider("Today's Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# 3. DYNAMIC SCALING LOGIC
# Mapping: Multiplier, Water Extra, Protein g/kg, Fat % of Calories, Steps, Workout Type
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "f": 0.30, "s": 4000, "ex": "Mobility & Stretching"},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.4, "f": 0.25, "s": 7000, "ex": "Brisk Walk & Yoga"},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "f": 0.25, "s": 10000, "ex": "Gym Training / Cardio"},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "f": 0.20, "s": 15000, "ex": "HIIT & Heavy Lifting"}
}
lvl = i_map[intensity]

# Math Engine
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)

# Macro Calculation
prot = int(w * lvl["p"])
fat_cals = cal * lvl["f"]
fat_grams = int(fat_cals / 9) # 9 calories per gram of fat
water = round((w * 0.035) + lvl["w"], 1)

# 4. DISPLAY DASHBOARD


c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fat Content", f"{fat_grams} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Steps:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")
st.success(f"🏋️ **Suggested Exercise:** {lvl['ex']}")

st.divider()

# 5. AI COACH (Workout + Diet)
if st.button("🚀 Ask AI Coach for Detailed Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing!")
    else:
        with st.spinner("AI analyzing metrics..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Diet & Workout Coach for {g}, {a}y, {w}kg. BMI {bmi}. Goal {goal}, {intensity} intensity. Provide {cuisine} menu for {cal}cal, {prot}g protein, {fat_grams}g fat. Suggest workout."
                res = model.generate_content(prompt)
                st.markdown(res.text)
                st.balloons()
            except:
                st.error("AI Busy. Use the scientific targets displayed above!")
