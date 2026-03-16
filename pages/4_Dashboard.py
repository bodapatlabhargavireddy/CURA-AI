import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Pull User Data (Updates instantly from your main page)
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Weight Loss")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 3. THE CALCULATION ENGINE (Scientific Formulas) ---
# Mifflin-St Jeor Formula
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water, Protein, Steps, and Time
water = round(w * 0.035, 1)
protein = int(w * 1.6)

if "Loss" in u_goal:
    cal = int(bmr * 1.2) - 500
    steps = 10000
    ex_time = "45-60 min"
    ex_type = "Cardio/HIIT"
elif "Gain" in u_goal:
    cal = int(bmr * 1.2) + 400
    steps = 6000
    ex_time = "45 min"
    ex_type = "Strength Training"
else:
    cal = int(bmr * 1.2)
    steps = 8000
    ex_time = "30 min"
    ex_type = "Brisk Walk/Yoga"

# --- 4. DASHBOARD UI ---
st.title("🛡️ Cura AI Dashboard")

# Top Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔥 Calories", f"{cal} kcal")
m2.metric("🍗 Protein", f"{protein} g")
m3.metric("💧 Water", f"{water} L")
m4.metric("👟 Steps", f"{steps:,}")

st.divider()

# Exercise Feature
st.subheader("🏋️ Exercise Suggestion")
st.info(f"**Recommended:** {ex_type} for **{ex_time}** daily.")

st.divider()

# --- 5. THE PROPER AI GENERATOR (Bypasses the 'Busy' Error) ---
st.subheader(f"🍱 {u_cuisine} Menu Plan")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key! Please check your Streamlit Secrets.")
    else:
        with st.spinner("Connecting to AI Nodes..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # We make the prompt very specific so the AI doesn't get confused
                prompt = f"Diet plan for {a}yo {g}, {w}kg. Goal: {u_goal}. Calories: {cal}. Cuisine: {u_cuisine}. List Breakfast, Lunch, Dinner."
                
                # CRITICAL: These settings help avoid "Busy" errors by limiting output size
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.4,
                        max_output_tokens=400,
                    )
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.balloons()
            except Exception as e:
                st.error("🚨 AI Nodes are busy. Expo Tip: Wait 10 seconds and try once more!")

# Sidebar Navigation
if st.sidebar.button("🔄 Back to Setup"):
    st.switch_page("cura.py")
