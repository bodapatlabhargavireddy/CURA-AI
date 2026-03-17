import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro Dashboard", layout="wide")

# 1. FETCH USER DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. DYNAMIC EXERCISE SELECTION
st.title("🛡️ Cura AI: Performance Dashboard")
st.subheader("Step 1: Select Today's Effort")

# This selection drives the math for everything else
ex_intensity = st.select_slider(
    "Select Exercise Intensity for today:",
    options=["Rest", "Light (Walk/Yoga)", "Moderate (Gym/Run)", "Heavy (Athlete/HIIT)"]
)

# 3. THE DYNAMIC LOGIC ENGINE
# Base BMR (Mifflin-St Jeor)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Multipliers based on intensity
if ex_intensity == "Rest":
    mult, water_extra, protein_mult, steps = 1.2, 0.0, 1.2, 3000
elif ex_intensity == "Light (Walk/Yoga)":
    mult, water_extra, protein_mult, steps = 1.375, 0.5, 1.4, 7000
elif ex_intensity == "Moderate (Gym/Run)":
    mult, water_extra, protein_mult, steps = 1.55, 1.0, 1.8, 10000
else: # Heavy
    mult, water_extra, protein_mult, steps = 1.725, 1.5, 2.2, 15000

# Final Calculations
cal_target = int(bmr * mult)
if "Loss" in u_goal: cal_target -= 400
if "Gain" in u_goal: cal_target += 400

protein_target = int(w * protein_mult)
water_target = round((w * 0.035) + water_extra, 1)

# 4. DISPLAY METRICS
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Total Calories", f"{cal_target} kcal", help="BMR + Activity Adjustment")
c2.metric("🍗 Protein Goal", f"{protein_target} g", help=f"{protein_mult}g per kg")
c3.metric("💧 Water Target", f"{water_target} L", help="Base + Sweat Compensation")
c4.metric("👟 Step Goal", f"{steps:,}")

# 5. THE AI MODEL (Incorporating Exercise Intensity)
st.divider()
st.subheader(f"🍱 Personalized {u_cuisine} Performance Menu")

if st.button("✨ Generate My Custom Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing! Add it to Streamlit Secrets.")
    else:
        with st.spinner("AI is calculating your metabolic needs..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # The prompt now includes the intensity so the AI changes the food!
                prompt = (f"Create a 1-day {u_cuisine} diet for a {w}kg {g} doing {ex_intensity} exercise. "
                         f"Goal: {u_goal}. Target: {cal_target} calories and {protein_target}g protein. "
                         f"Format as Breakfast, Lunch, Dinner.")
                
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 500, "temperature": 0.7}
                )
                st.markdown(response.text)
                st.balloons()
            except Exception:
                st.error("🚨 AI Nodes Busy. Please wait 10s and try again.")

if st.sidebar.button("🔄 Reset Profile"):
    st.switch_page("cura.py")
