import streamlit as st
import google.generativeai as genai
import os

# 1. Page Config
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Stronger API Configuration
# Using 'rest' transport is the secret to stopping timeouts on public/expo WiFi
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("❌ API Key Missing in Secrets!")
    st.stop()

st.title("🛡️ Cura AI Health Hub")

# --- DATA RETRIEVAL ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])
goal = st.session_state.get("goal", "Maintenance")

# --- CALCULATIONS ---
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)
if "Weight Loss" in goal: tdee -= 500
elif "Weight Gain" in goal: tdee += 400

# --- DISPLAY TOP METRICS ---
st.subheader("🚀 Your Daily Health Targets")
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{tdee} kcal")
c2.metric("💧 Water", f"{round(w * 0.035, 1)} L")
c3.metric("🍗 Protein", f"{int(w * 1.5)} g")
c4.metric("👟 Steps", "10,000" if "BP" in goal or "PCOD" in goal else "8,000")

st.divider()

# --- MONITORING INPUTS ---
st.subheader("💓 Live Vitals")
m1, m2, m3 = st.columns(3)
with m1: hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
with m2: bp = st.number_input("Systolic BP", 80, 200, 120)
with m3: water_drunk = st.slider("Water Consumed (L)", 0.0, 5.0, 1.5)

st.divider()
# --- THE AI FOOD MENU (FIXED 404 & VERSION ERROR) ---
st.subheader(f"🍱 AI {cuisine} Menu for {goal}")

if st.button("✨ Generate AI Medical Menu"):
    try:
        # Using 'models/' prefix is MANDATORY for some API versions to avoid 404
        # 'gemini-1.5-flash' is the correct string for the latest library
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = f"""
        CONTEXT: Clinical Nutritionist Assistant
        USER: {g}, {a}yrs, {w}kg. 
        GOAL: {goal}. 
        MEDICAL: {meds}. 
        VITALS: BP {bp}, HR {hr}.
        CUISINE: {cuisine}.
        CALORIE TARGET: {tdee} kcal.
        
        TASK: Provide a 1-day meal menu (Breakfast, Lunch, Dinner, Snack).
        Include calorie counts and WHY these foods help with {goal}.
        """

        with st.spinner("Cura AI is calculating..."):
            # Using generate_content with a direct call
            response = model.generate_content(
                prompt,
                request_options={"timeout": 60}
            )
            
            if response.text:
                st.markdown(response.text)
                st.success("✅ Personalized Menu Generated Successfully")
                st.link_button(f"Order {cuisine} on Zomato", f"https://www.zomato.com/search?q=healthy+{cuisine}")
            else:
                st.error("The AI responded but the content was empty. Try again.")

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            st.error("🚨 API Path Error (404).")
            st.info("Trying backup model: gemini-pro...")
            # Fallback to the older stable model name if Flash is not recognized
            try:
                model_alt = genai.GenerativeModel('models/gemini-pro')
                response_alt = model_alt.generate_content(prompt)
                st.markdown(response_alt.text)
            except Exception as e2:
                st.error(f"Critical API Error: {e2}")
        else:
            st.error(f"Error: {error_msg}")
