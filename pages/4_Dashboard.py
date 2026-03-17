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

# 2. LOCAL SCIENCE ENGINE (Instant)
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Clinical Dashboard")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic Mapping
i_map = {
    "Rest": {"m": 1.2, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "p": 1.4, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# Math Engine
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round(w * 0.035 + (0.8 if intensity != "Rest" else 0), 1)

# 3. DISPLAY DASHBOARD

c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fat Content", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")
st.divider()

# 4. DIRECT AI CALL (Optimized)
if st.button("🚀 Generate AI Meal & Exercise Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing!")
    else:
        with st.spinner("AI Coach is connecting..."):
            try:
                # Direct simple configuration
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Simple prompt for high-speed response
                prompt = (f"Provide a 1-day {cuisine} meal plan and a 45min workout "
                          f"for a {g}, {a}yo, {w}kg. BMI {bmi}. Goal: {goal}. "
                          f"Intensity: {intensity}. Targets: {cal}kcal, {prot}g protein, {fat_g}g fat.")
                
                response = model.generate_content(prompt)
                
                if response:
                    st.markdown(response.text)
                    st.balloons()
            except Exception:
                st.error("AI Server Busy. Please wait 10 seconds and try again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
