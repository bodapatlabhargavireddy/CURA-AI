import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- 1. API CONFIG ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key Missing!")

# --- 2. DATA RETRIEVAL (PULLING FROM SETUP PAGE) ---
# We use .get() to avoid errors if the user skips the setup page
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Maintenance")
cuisine = st.session_state.get("cuisine", "Indian")

# --- 3. DYNAMIC CALCULATIONS ---
# These change for EVERY user based on their input
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Adjust Calories and Steps based on Goal
if goal == "Weight Loss":
    tdee = int(bmr * 1.2) - 500
    steps = 10000
elif goal == "Weight Gain":
    tdee = int(bmr * 1.2) + 400
    steps = 6000
else:
    tdee = int(bmr * 1.2)
    steps = 8000

water = round(w * 0.035, 1)
protein = int(w * 1.6)

# --- 4. UI DISPLAY ---
st.title("🛡️ Your Personalized Cura Hub")

# Visual confirmation that the code is reading YOUR inputs
st.info(f"📋 Profile: {w}kg | {h}cm | {g} | Goal: {goal}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Daily Calories", f"{tdee} kcal")
col2.metric("💧 Water Intake", f"{water} L")
col3.metric("🍗 Protein Goal", f"{protein} g")
col4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# --- 5. MONITORING & PROGRESS ---
st.subheader("💓 Live Vitals")
m1, m2, m3 = st.columns(3)
with m1: hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
with m2: bp = st.number_input("Systolic BP", 80, 200, 120)
with m3: 
    # Compare original weight with today's weight
    current_w = st.number_input("Log Today's Weight (kg)", 30.0, 200.0, float(w))
    diff = round(current_w - w, 2)
    if diff != 0: st.write(f"Weight Change: {diff} kg")

st.divider()

# --- 6. AI FOOD MENU ---
st.subheader(f"🍱 Personalized {cuisine} Food Menu")

if st.button("✨ Generate AI Food Menu"):
    with st.spinner("AI is analyzing your profile..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # This prompt ensures the AI uses the UNIQUE data
            prompt = f"""
            Act as a Nutritionist. 
            User: {g}, {a}yrs, {w}kg (current: {current_w}kg). 
            Goal: {goal}. Cuisine: {cuisine}.
            Vitals: BP {bp}, HR {hr}. Target: {tdee} calories.
            Provide a 1-day food menu (Breakfast, Lunch, Dinner, Snack).
            """
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.success("✅ Menu created for your unique profile!")
            
        except Exception as e:
            st.error("AI Node Busy. Trying backup...")
            # Simple fallback to gemini-pro if flash is busy
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                res = model_alt.generate_content(prompt)
                st.markdown(res.text)
            except:
                st.error("Connection Error. Check API Key.")
