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

# 2. INSTANT SCIENCE ENGINE
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic Mapping
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.4, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + lvl["w"], 1)

# 3. DISPLAY DASHBOARD

c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fat Content", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Steps:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")

# 4. THE "CLEAN CALL" AI MODEL
st.divider()
if st.button("🚀 Generate AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key!")
    else:
        with st.spinner("AI is thinking..."):
            try:
                # Direct Configuration (No extra parameters to slow it down)
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Simplified Prompt - Shortest possible length for fastest response
                msg = f"Give a 45m workout and {cuisine} menu for {cal}cal, {prot}g protein, {fat_g}g fat. Goal: {goal}."
                
                response = model.generate_content(msg)
                
                if response.text:
                    st.success("✅ AI Plan Ready")
                    st.markdown(response.text)
                    st.balloons()
            except Exception as e:
                # If the AI is literally down, this gives a professional fallback
                st.error("⚠️ AI Cloud is busy. Showing Local Science Plan...")
                st.write(f"### 📋 Instant Plan for {intensity} Day")
                st.write(f"- **Focus:** Increase protein to {prot}g to support muscle.")
                st.write(f"- **Hydration:** Drink {water}L to maintain metabolic rate.")
                st.write(f"- **Exercise:** Focus on hitting {lvl['s']:,} steps today.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
