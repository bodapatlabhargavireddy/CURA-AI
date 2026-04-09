import streamlit as st
import google.generativeai as genai

# --- 1. DATA RECOVERY ---
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")
diet_type = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")
hc = st.session_state.get("final_conditions", ["None"])

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Data Sync Error. Please restart from the home page.")
    st.stop()

# --- 2. CALCULATIONS ---
st.title("🛡️ Cura AI: Performance Coach")

intensity = st.select_slider("Select Intensity:", options=["Rest", "Light", "Moderate", "Heavy"], value="Moderate")

i_map = {
    "Rest": {"mult": 1.2, "prot": 1.2, "steps": 4000},
    "Light": {"mult": 1.375, "prot": 1.5, "steps": 7000},
    "Moderate": {"mult": 1.55, "prot": 1.8, "steps": 10000},
    "Heavy": {"mult": 1.725, "prot": 2.2, "steps": 15000}
}
lvl = i_map[intensity]

protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 3. UI DASHBOARD ---
st.info(f"📋 **Profile:** {w}kg {g} | **Goal:** {goal}")

c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("👟 Step Goal", f"{step_goal:,}")

st.divider()

# --- 4. THE AI GENERATOR (Strict AI Only) ---
if "final_ai_plan" not in st.session_state:
    st.session_state.final_ai_plan = None

if st.button("🚀 Generate Personalized AI Plan"):
    with st.spinner("Connecting to Gemini AI..."):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Focused prompt to include Step Count and Diet
            prompt = (
                f"Create a 1-day {cuisine} {diet_type} plan for {g}, {w}kg. "
                f"Goal: {goal}. Medical: {hc}. "
                f"Targets: {cal}kcal, {protein_target}g protein. "
                f"IMPORTANT: Include a workout to hit {step_goal} steps."
            )
            
            response = model.generate_content(prompt)
            st.session_state.final_ai_plan = response.text
            st.balloons()
            
        except Exception as e:
            st.error("🚨 API Busy. Please wait 30 seconds and try again.")

# --- 5. DISPLAY AI PLAN ---
if st.session_state.final_ai_plan:
    st.markdown("### 🥗 Your Personalized AI Schedule")
    st.markdown(st.session_state.final_ai_plan)

# Sidebar reset for a clean start
if st.sidebar.button("🔄 Start New Assessment"):
    st.session_state.clear()
    st.switch_page("cura.py")
    
