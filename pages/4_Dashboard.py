import streamlit as st
import google.generativeai as genai

st.set_page_config(initial_sidebar_state="expanded") # Sidebar returns here

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🛡️ Cura Dashboard")

# 1. Calculation
w = st.session_state.get("weight", 70)
h = st.session_state.get("height", 170)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")

s = 5 if g == "Male" else -161
tdee = int(((10 * w) + (6.25 * h) - (5 * a) + s) * 1.3)

# 2. Display
c1, c2, c3 = st.columns(3)
c1.metric("Daily Calories", f"{tdee} kcal")
c2.metric("Protein", f"{int(w * 1.6)}g")
c3.metric("Water", f"{round(w * 0.035, 1)} L")

st.divider()

# 3. AI Meal Plan & App Suggestions
if st.button("🥘 Generate AI Meal Plan"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"1-day {st.session_state.get('cuisine')} plan for {tdee} cal. Medical: {st.session_state.get('meds')}."
    response = model.generate_content(prompt)
    st.markdown(response.text)
    
    st.info("🔗 **Order on Zomato:**")
    st.link_button("Find Healthy Meals", f"https://www.zomato.com/search?q=Healthy+food")
