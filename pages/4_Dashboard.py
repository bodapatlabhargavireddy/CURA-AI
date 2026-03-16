import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key Missing!")

st.title("🛡️ Cura Health Hub & Live Monitor")

# --- DATA RETRIEVAL ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])
goal = st.session_state.get("goal", "Maintenance")

# --- CALCULATION LOGIC ---
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)
if "Weight Loss" in goal: tdee -= 500
elif "Weight Gain" in goal: tdee += 400

# --- FEATURE 1: 4 KEY METRICS ---
st.subheader("🚀 Your Daily Health Targets")
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{tdee} kcal")
c2.metric("💧 Water Goal", f"{round(w * 0.035, 1)} L")
c3.metric("🍗 Protein", f"{int(w * 1.4)} g")
c4.metric("👟 Step Goal", "10,000" if "BP" in goal or "PCOD" in goal else "8,000")

st.divider()

# --- FEATURE 2: LIVE MONITORING (VITALS) ---
st.subheader("💓 Real-Time Vitals Tracking")
m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
    if hr > 100: st.error("🚩 High Heart Rate Alert")
with m_col2:
    bp = st.number_input("Systolic BP (Upper)", 80, 200, 120)
    if bp > 140: st.error("🚩 Hypertension Warning")
with m_col3:
    water_drunk = st.slider("Water Consumed (Liters)", 0.0, 5.0, 1.5, 0.25)

st.divider()

# --- FEATURE 3: AI FOOD MENU (ANTI-TIMEOUT VERSION) ---
st.subheader(f"🍱 AI Generated {cuisine} Food Menu")

if st.button("Generate Medical-Grade Meal Plan"):
    # 1. Faster Configuration
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest') # Use 'rest' for more stable connections
    
    model = genai.GenerativeModel('gemini-1.5-flash') # Flash is 3x faster than Pro
    
    # 2. Optimized (Shorter) Prompt to reduce processing time
    fast_prompt = f"""
    Create a 1-day {cuisine} menu for {goal} ({tdee} cal). 
    Context: {meds}, BP:{bp}, HR:{hr}.
    Format: B/L/D with calories. Keep it concise.
    """

    success = False
    with st.spinner("⚡ Cura AI is optimizing connection..."):
        try:
            # We wrap this in a 30-second timeout to give it enough time
            response = model.generate_content(
                fast_prompt,
                request_options={"timeout": 30} 
            )
            
            if response.text:
                st.markdown(response.text)
                st.success("✅ Menu Generated!")
                success = True
        except Exception as e:
            # If AI fails, we show a 'Static' plan so you don't look bad at the Expo
            st.error("🚨 AI is taking too long to respond.")
            st.warning("🔄 Showing a high-speed backup plan instead:")
            
            # --- BACKUP PLAN (ALWAYS WORKS) ---
            st.markdown(f"""
            **High-Fiber {cuisine} Plan:**
            * **Breakfast:** Sprouted grains or Oats (350 cal)
            * **Lunch:** Grilled protein with {cuisine} spices & salad (600 cal)
            * **Dinner:** Clear soup & steamed veggies (400 cal)
            * **Health Tip:** Drink 500ml water before every meal for {goal}.
            """)

    if success:
        st.link_button(f"Order Healthy {cuisine} on Zomato", f"https://www.zomato.com/search?q=healthy+{cuisine}")
# Sidebar Navigation
if st.sidebar.button("🔄 Restart Assessment"):
    st.session_state.clear()
    st.switch_page("cura.py")
