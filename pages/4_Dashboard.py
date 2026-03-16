import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- 1. CLEAN API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    # REMOVED transport='rest' to fix the 404 URL error
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing!")
    st.stop()

st.title("🛡️ Cura AI Health Hub")

# --- DATA RETRIEVAL (Same as before) ---
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

# --- DISPLAY METRICS ---
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

# --- THE AI FOOD MENU (FIXED 404) ---
st.subheader(f"🍱 AI {cuisine} Menu for {goal}")

if st.button("✨ Generate AI Medical Menu"):
    with st.spinner("Cura AI is connecting..."):
        try:
            # Use the simplest model name possible
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Create a 1-day {cuisine} meal plan for a {g}, {a}yrs, {w}kg. 
            Goal: {goal}. Medical: {meds}. Vitals: BP {bp}, HR {hr}.
            Target: {tdee} calories. 
            Include Breakfast, Lunch, Dinner, and why this helps {goal}.
            """

            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.success("✅ Menu Generated!")
                st.link_button(f"Order on Zomato", f"https://www.zomato.com/search?q=healthy+{cuisine}")
            else:
                st.error("Empty response. Please try again.")

        except Exception as e:
            # This will show us if it's an API Key issue or a Network issue
            st.error(f"Technical Error: {str(e)}")
            st.info("Check your Streamlit Secrets for any extra spaces in the API Key.")
