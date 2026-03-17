import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. DATA RECOVERY
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. LOCAL SCIENCE ENGINE (Instant)
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Dashboard")
intensity = st.select_slider("Activity Level Today:", options=["Rest", "Light", "Moderate", "Heavy"])

# 3. DYNAMIC SCALING LOGIC
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# The Math
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_grams = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + lvl["w"], 1)

# 4. DISPLAY DASHBOARD


c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fat Content", f"{fat_grams} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Steps:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")

st.divider()

# 5. OPTIMIZED AI COACH (Workout + Diet)
if st.button("🚀 Generate AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("AI Coach is analyzing performance data..."):
            # RE-TRY LOGIC TO BEAT THE BUSY MESSAGE
            success = False
            for i in range(2): 
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Short, direct prompt for speed
                    prompt = f"Coach for {g}, {w}kg. BMI {bmi}. Goal: {goal}. Intensity: {intensity}. Targets: {cal}cal, {prot}g protein, {fat_grams}g fat. Provide 45m workout and {cuisine} meal plan."
                    
                    # Lower temperature makes the AI faster and more stable
                    res = model.generate_content(
                        prompt, 
                        generation_config={"temperature": 0.2, "max_output_tokens": 500}
                    )
                    st.markdown(res.text)
                    st.balloons()
                    success = True
                    break
                except:
                    time.sleep(2) # Wait 2 seconds and try one more time
            
            if not success:
                st.error("AI is busy. Please show the judges the local targets above!")
