import streamlit as st
import google.generativeai as genai

# --- 1. STRICT DATA RECOVERY ---
# We use None as default. If it's None, we know they skipped a step.
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Incomplete Profile. Please restart the assessment.")
    st.button("Restart", on_click=lambda: st.switch_page("cura.py"))
    st.stop()

# --- 2. DYNAMIC CALCULATIONS ---
# Protein: Multipliers based on strict activity
intensity = st.select_slider("Select Today's Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

prot_map = {"Rest": 1.2, "Light": 1.5, "Moderate": 1.8, "Heavy": 2.2}
protein_target = round(w * prot_map[intensity], 1)

# Steps
steps = {"Rest": 4000, "Light": 7000, "Moderate": 10000, "Heavy": 15000}[intensity]

# Water (4% of body weight + activity boost)
water = round((w * 0.04) + {"Rest": 0, "Light": 0.5, "Moderate": 0.8, "Heavy": 1.2}[intensity], 1)

# Calories
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * {"Rest": 1.2, "Light": 1.375, "Moderate": 1.55, "Heavy": 1.725}[intensity])

# Goal Offset
if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 3. DYNAMIC UI ---
st.title("🛡️ Cura AI: Performance Coach")
# Heading is now 100% based on the user's specific choice
st.subheader(f"Strategy: {goal}")

st.info(f"📊 **System Status:** Analyzing {w}kg {g} | {a} years old")

c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water} L")

st.write("### 👟 Activity Target")
st.metric("Daily Steps", f"{steps:,} steps")

st.divider()

# --- 4. AI PROMPT  ---
if st.button("🚀 Generate AI Analysis"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (f"User: {g}, {w}kg, {a}yo. Goal: {goal}. Intensity: {intensity}. "
                  f"Provide 1-day meal plan for {cal}cal and {protein_target}g protein. "
                  f"Include a workout hitting {steps} steps.")
        
        response = model.generate_content(prompt)
        st.markdown(response.text)
    except:
        st.warning("Switching to Local Engine due to API limit.")
        st.write(f"Target {cal} kcal and {protein_target}g protein today.")
