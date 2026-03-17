import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Coach", layout="wide")

# 1. FETCH DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Weight Loss")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. LOCAL CALCULATIONS (BMI, FAT, CALORIES)
bmi = round(w / ((h/100)**2), 1)
if bmi < 18.5: status = "Underweight"
elif bmi < 25: status = "Healthy"
elif bmi < 30: status = "Overweight"
else: status = "Obese"

# Body Fat Estimate
bf = round((1.20 * bmi) + (0.23 * a) - (16.2 if g == "Male" else 5.4), 1)

# Base BMR
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# 3. UI - INTENSITY SLIDER
st.title("🛡️ Cura AI: Total Coach")
intensity = st.select_slider("Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Adjustment Mapping
i_map = {
    "Rest": {"mul": 1.2, "wat": 0.0, "step": 4000, "prot": 1.4},
    "Light": {"mul": 1.375, "wat": 0.5, "step": 7000, "prot": 1.6},
    "Moderate": {"mul": 1.55, "wat": 1.0, "step": 10000, "prot": 1.8},
    "Heavy": {"mul": 1.725, "wat": 1.5, "step": 15000, "prot": 2.2}
}
lvl = i_map[intensity]

cal_target = int(bmr * lvl["mul"]) + (400 if "Gain" in u_goal else -500 if "Loss" in u_goal else 0)
prot_target = int(w * lvl["prot"])
wat_target = round((w * 0.035) + lvl["wat"], 1)

# 4. DISPLAY METRICS
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚖️ BMI", f"{bmi} ({status})")
c2.metric("🔥 Calories", f"{cal_target}")
c3.metric("🍗 Protein", f"{prot_target}g")
c4.metric("💧 Water", f"{wat_target}L")

st.divider()

# 5. AI COACH (Workout + Diet)
if st.button("🚀 Generate AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key")
    else:
        with st.spinner("AI is thinking..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Simplified single-line prompt to avoid syntax issues
                p = f"Coach for {g}, {a}y, {w}kg. BMI {bmi}, Goal {u_goal}, {intensity} intensity. Suggest 45m workout and {u_cuisine} menu for {cal_target}kcal and {prot_target}g protein."
                
                config = genai.types.GenerationConfig(temperature=0.2, max_output_tokens=500)
                response = model.generate_content(p, generation_config=config)
                
                st.markdown(response.text)
                st.balloons()
            except:
                st.error("AI Busy. Wait 10s and try again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
