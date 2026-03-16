import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Cura AI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. API Configuration (Using standard stable setup)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing in Streamlit Secrets!")
    st.stop()

st.title("🛡️ Cura AI Health Hub")

# --- 3. DYNAMIC DATA RETRIEVAL ---
# These pull from your previous pages. If no data is found, it uses defaults.
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Maintenance")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])

# --- 4. THE CALCULATION ENGINE (The "Personalizer") ---
# Mifflin-St Jeor Equation
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3) # Base calories for sedentary activity

# Adjust Calories and Steps based on User Goal
if "Weight Loss" in goal:
    tdee -= 500
    step_goal = 10000
elif "Weight Gain" in goal:
    tdee += 400
    step_goal = 6000
else:
    step_goal = 8000

# Water: 35ml per kg of body weight
water_goal = round(w * 0.035, 1)

# Protein: 1.5g per kg of body weight
protein_goal = int(w * 1.5)

# --- 5. DISPLAY: DYNAMIC METRICS ---
st.subheader("🚀 Your Personalized Daily Targets")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Calories", f"{tdee} kcal")
with col2:
    st.metric("💧 Water", f"{water_goal} L")
with col3:
    st.metric("🍗 Protein", f"{protein_goal} g")
with col4:
    st.metric("👟 Steps", f"{step_goal:,}")

st.divider()

# --- 6. LIVE MONITORING (VITALS) ---
st.subheader("💓 Live Vitals & Progress")
m1, m2, m3 = st.columns(3)

with m1:
    hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
    if hr > 100: st.error("🚩 High Heart Rate Alert")
with m2:
    bp = st.number_input("Systolic BP (Upper)", 80, 200, 120)
    if bp > 140: st.error("🚩 Hypertension Warning")
with m3:
    # Tracking current weight vs starting weight
    cur_w = st.number_input("Current Weight (kg)", 30.0, 200.0, float(w))
    diff = round(cur_w - w, 2)
    if diff != 0:
        st.info(f"Change: {diff} kg")

st.divider()

# --- 7. AI FOOD MENU GENERATOR ---
st.subheader(f"🍱 Personalized {cuisine} Food Menu")

if st.button("✨ Generate AI Food Menu"):
    with st.spinner("AI is analyzing your vitals and progress..."):
        # Structured prompt to ensure the AI uses the dynamic data
        prompt = f"""
        Act as a Clinical Dietician. 
        User: {g}, {a}yrs, {w}kg (Current: {cur_w}kg). 
        Goal: {goal}. Medical: {meds}.
        Vitals: BP {bp}, HR {hr}. Target: {tdee} kcal.
        
        Task: Create a 1-day {cuisine} Food Menu.
        Include Breakfast, Lunch, Dinner, and 1 Snack with calorie counts.
        Adjust the menu if current weight {cur_w} differs from starting weight {w}.
        """

        try:
            # Auto-recovery logic for the 404/Node Busy error
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.success("✅ Food Menu Generated!")
                st.link_button("Order Healthier on Zomato", f"https://www.zomato.com/search?q=healthy+{cuisine}")
            else:
                st.error("AI node returned empty results. Try again.")

        except Exception as e:
            # Fallback for API Model Version errors
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response_alt = model_alt.generate_
