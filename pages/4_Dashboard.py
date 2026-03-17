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

# 2. LOCAL SCIENCE ENGINE
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI Dashboard")
intensity = st.select_slider("Activity Level:", options=["Rest", "Light", "Moderate", "Heavy"])

# Intensity Logic
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# Math
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + lvl["w"], 1)

# 3. DISPLAY METRICS
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fats", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")

# 4. THE AI MODEL (Optimized for Speed)
st.divider()
if st.button("🚀 Generate AI Workout & Meal Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("Connecting to AI..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                # Use a smaller, faster model configuration
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # The "Perfect" prompt for high-speed response
                prompt = f"Context: {g}, {w}kg, BMI {bmi}, Goal {goal}, {intensity} intensity. Task: Provide a 3-sentence workout and a {cuisine} menu for {cal}cal, {prot}g protein, {fat_g}g fat."
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.1,  # Lower = Faster and more consistent
                        max_output_tokens=400
                    )
                )
                
                if response.text:
                    st.success("✅ AI Coaching Plan Ready")
                    st.markdown(response.text)
                    st.balloons()
                else:
                    st.warning("AI returned an empty response. Try once more.")
                    
            except Exception as e:
                st.error(f"AI Temporary Error. Use local targets above while the server resets.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
