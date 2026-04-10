import streamlit as st
import google.generativeai as genai
import time

# --- 1. API CONFIGURATION ---
# Make sure your secret key is named "GEMINI_API_KEY" in Streamlit Cloud
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key missing! Check your st.secrets.")

# --- 2. DATA RECOVERY ---
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")
health = st.session_state.get("final_conditions", ["None"])
diet = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Profile incomplete. Please restart.")
    st.stop()

# --- 3. CALCULATIONS ---
st.title("🛡️ Cura AI: Performance Coach")

intensity = st.select_slider("Select Intensity:", options=["Rest", "Light", "Moderate", "Heavy"], value="Moderate")

i_map = {
    "Rest": {"mult": 1.2, "prot": 1.2, "steps": 4000, "water": 0.0},
    "Light": {"mult": 1.375, "prot": 1.5, "steps": 7000, "water": 0.5},
    "Moderate": {"mult": 1.55, "prot": 1.8, "steps": 10000, "water": 0.8},
    "Heavy": {"mult": 1.725, "prot": 2.2, "steps": 15000, "water": 1.2}
}
lvl = i_map[intensity]

# Math Engine (Deterministic)
protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]
water_target = round((w * 0.04) + lvl["water"], 1)

s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

if "Loss" in goal: cal -= 500
elif "Gain" in goal: cal += 400

# --- 4. UI DASHBOARD ---
st.info(f"📋 **Strategy:** {goal} | {w}kg {g}")

c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water Intake", f"{water_target} L")

st.write("### 👟 Activity Goal")
st.metric("Steps Required", f"{step_goal:,}", delta=f"{intensity} Level")

st.divider()

# --- 5. THE AI GENERATOR (WITH RETRY LOGIC) ---
if "final_ai_plan" not in st.session_state:
    st.session_state.final_ai_plan = None

if st.button("🚀 Generate AI Plan"):
    with st.spinner("Processing Biological Data..."):
        # TRY THIS MODEL STRING FIRST
        try:
            # Adding 'models/' prefix fixes the 404 error in most SDK versions
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            prompt = (
                f"User: {g}, {w}kg. Goal: {goal}. Diet: {diet} ({cuisine}). "
                f"Medical: {health}. Targets: {cal}kcal, {protein_target}g protein, {water_target}L water. "
                f"Provide a short 24-hour meal and workout plan. Use bold headers."
            )

            success = False
            for attempt in range(3):
                try:
                    # Explicitly calling the content generation
                    response = model.generate_content(prompt)
                    st.session_state.final_ai_plan = response.text
                    success = True
                    break 
                except Exception as e:
                    if "429" in str(e):
                        st.warning(f"Rate limit hit. Retrying in {5 * (attempt + 1)}s...")
                        time.sleep(5 * (attempt + 1))
                    else:
                        st.error(f"Generation Error: {e}")
                        break
            
            if success:
                st.balloons()
            
        except Exception as model_err:
            st.error(f"Model Initialization Error: {model_err}")
            st.info("Try changing model name to 'gemini-1.5-flash' (without models/ prefix) if this persists.")

if st.session_state.final_ai_plan:
    st.markdown(st.session_state.final_ai_plan)
