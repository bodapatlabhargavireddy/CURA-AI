import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI", layout="wide")

# 1. Pull data from Step 1
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. Quick Calculations
water = round(w * 0.035, 1)
protein = int(w * 1.6)
steps = 10000 if "Loss" in goal else (5000 if "Gain" in goal else 8000)
ex_time = "45-60 min" if "Loss" in goal else "45 min"

# 3. UI
st.title("📊 Your Health Dashboard")
st.write(f"**Targeting:** {goal} | **Water:** {water}L | **Steps:** {steps}")

st.info(f"🏋️ **Daily Exercise:** {ex_time} of targeted activity.")

st.divider()

# 4. AI Menu
if st.button("✨ Generate My Menu"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"1-day {cuisine} diet for {w}kg {g}, goal: {goal}. Brief Breakfast, Lunch, Dinner."
        
        with st.spinner("AI is generating..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    except:
        st.error("🚨 Server busy. Please wait 10 seconds and try again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
