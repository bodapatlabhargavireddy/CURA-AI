import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- DATA RETRIEVAL (The fix for updated user input) ---
u_weight = st.session_state.get("weight", 70.0)
u_height = st.session_state.get("height", 170.0)
u_age = st.session_state.get("age", 25)
u_gender = st.session_state.get("gender", "Male")

# --- DYNAMIC CALCULATIONS ---
# 1. BMI Calculation
u_bmi = round(u_weight / ((u_height/100)**2), 1)

# 2. Calorie Calculation (Mifflin-St Jeor)
s = 5 if u_gender == "Male" else -161
u_cal = int((10 * u_weight) + (6.25 * u_height) - (5 * u_age) + s)

# 3. Protein Calculation
u_protein = int(u_weight * 1.6)

# --- DISPLAY ---
st.title("🍱 Food Menu Dashboard")

# Showing the calculated BMI clearly
st.info(f"Summary for {u_weight}kg: BMI is {u_bmi} | Target: {u_cal} kcal")

col1, col2 = st.columns(2)
col1.metric("🔥 Calories", f"{u_cal} kcal")
col2.metric("🍗 Protein", f"{u_protein} g")

st.divider()

# --- AI GENERATION ---
if st.button("✨ Generate My Food Menu"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # We send the UPDATED values to the AI
        prompt = f"Create a 1-day food menu for {u_weight}kg, {u_gender}, {u_age}yrs. Target {u_cal} kcal."
        response = model.generate_content(prompt)
        st.markdown(response.text)
    except:
        st.error("AI Busy.")
