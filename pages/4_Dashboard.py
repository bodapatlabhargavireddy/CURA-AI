import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- 1. PULL DATA FROM MEMORY ---
# These variables now grab exactly what the user typed on page 1
u_weight = st.session_state.get("weight", 70.0)
u_height = st.session_state.get("height", 170.0)
u_age = st.session_state.get("age", 25)
u_gender = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")

# --- 2. THE MATH (THIS MAKES VALUES DIFFERENT FOR EVERYONE) ---
# Mifflin-St Jeor Formula
s = 5 if u_gender == "Male" else -161
bmr = (10 * u_weight) + (6.25 * u_height) - (5 * u_age) + s

# Calculate Calories based on goal
if "Weight Loss" in u_goal:
    total_calories = int(bmr * 1.2) - 500
    steps = 10000
elif "Weight Gain" in u_goal:
    total_calories = int(bmr * 1.2) + 400
    steps = 6000
else:
    total_calories = int(bmr * 1.2)
    steps = 8000

# Calculate Water (35ml per kg)
water = round(u_weight * 0.035, 1)

# Calculate Protein (1.6g per kg)
protein = int(u_weight * 1.6)

# --- 3. DISPLAY THE UNIQUE METRICS ---
st.title("🛡️ Your Personalized Cura Hub")
st.info(f"Showing results for: {u_weight}kg, {u_height}cm, {u_gender}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Daily Calories", f"{total_calories} kcal")
c2.metric("💧 Water Intake", f"{water} L")
c3.metric("🍗 Protein Goal", f"{protein} g")
c4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# --- 4. LIVE MONITORING & PROGRESS ---
st.subheader("💓 Real-Time Vitals")
m1, m2, m3 = st.columns(3)
with m1: hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
with m2: bp = st.number_input("Systolic BP", 80, 200, 120)
with m3: 
    current_w = st.number_input("Log Today's Weight (kg)", 30.0, 200.0, float(u_weight))
    # AI logic: Did weight change?
    diff = round(current_w - u_weight, 2)
    if diff != 0: st.write(f"Weight Change: {diff} kg")

# --- 5. AI FOOD MENU ---
if st.button("🍱 Generate My Food Menu"):
    # This ensures the AI also sees the UNIQUE values
    prompt = f"Create a {u_goal} meal plan for {u_weight}kg, {u_gender}, BP {bp}, HR {hr}. Target {total_calories} cal."
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.markdown(response.text)
    except:
        st.error("AI Node Busy.")
