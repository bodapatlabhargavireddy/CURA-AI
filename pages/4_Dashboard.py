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

# 2. THE SCIENCE ENGINE (Local & Instant)
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Total Performance Coach")
intensity = st.select_slider("Daily Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic Mapping for Macros and Steps
i_map = {
    "Rest": {"m": 1.2, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# Math Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + (1.0 if intensity == "Heavy" else 0.5 if intensity != "Rest" else 0), 1)

# 3. DISPLAY DASHBOARD

c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fats", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")
st.divider()

# 4. STABLE AI GENERATOR
if st.button("🚀 Generate AI Workout & Meal Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Streamlit Secrets!")
    else:
        with st.spinner("AI is calculating your plan..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # The most stable prompt format possible
                prompt = (f"Coach: Give 1-day {cuisine} menu and 45m workout for {g}, {w}kg. "
                          f"BMI: {bmi}, Goal: {goal}, Intensity: {intensity}. "
                          f"Target: {cal}cal, {prot}g protein, {fat_g}g fat. Be concise.")
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.session_state.last_plan = response.text
                    st.success("✅ AI Plan Generated")
                    st.markdown(response.text)
                    st.balloons()
            except Exception:
                st.error("AI Busy. Using standard scientific targets (shown above).")
                st.info("💡 Tip: Wait 15 seconds before clicking again to reset the API limit.")

# Maintain plan on screen if it exists
elif "last_plan" in st.session_state:
    st.markdown(st.session_state.last_plan)

if st.sidebar.button("🔄 Restart"):
    st.session_state.clear()
    st.switch_page("cura.py")
