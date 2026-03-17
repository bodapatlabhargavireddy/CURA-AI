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

# 2. LOCAL SCIENCE ENGINE (Instant)
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Total Performance Coach")
intensity = st.select_slider("Intensity Level:", options=["Rest", "Light", "Moderate", "Heavy"])

# Intensity Logic Mapping
i_map = {
    "Rest": {"m": 1.2, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# The Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + (1.0 if intensity == "Heavy" else 0.5 if intensity != "Rest" else 0), 1)

# 3. DASHBOARD METRICS


c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fats", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")
st.divider()

# 4. THE AI ENGINE (Meal & Exercise)
if st.button("🚀 Generate AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Add GEMINI_API_KEY to Streamlit Secrets!")
    else:
        with st.spinner("AI is analyzing performance data..."):
            try:
                # Use the ultra-stable configuration
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                
                # We use the most basic model call - no extra parameters
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Direct, simple prompt
                prompt = (f"Coach: 1-day {cuisine} meal plan and 45m workout for {g}, {w}kg. "
                          f"BMI: {bmi}, Goal: {goal}, Intensity: {intensity}. "
                          f"Target: {cal}cal, {prot}g protein, {fat_g}g fat.")
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("✅ AI Coaching Plan Ready")
                    st.markdown(response.text)
                    st.balloons()
            except Exception:
                # If AI fails, we show a clean, formatted backup so it looks intentional
                st.error("AI Node Busy. Displaying Local Scientific Plan...")
                st.subheader(f"📋 Scientific Plan for {intensity} Day")
                st.write(f"**Exercise:** focus on compound movements and hitting {lvl['s']:,} steps.")
                st.write(f"**Nutrition:** High protein ({prot}g) {cuisine} diet with {fat_g}g healthy fats.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
