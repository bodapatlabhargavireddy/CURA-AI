import streamlit as st
import google.generativeai as genai

# --- 1. CLEAN API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    # We use the default configuration to avoid the v1beta URL error
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
# --- THE AI FOOD MENU (FIXED & RENAMED) ---
st.subheader(f"🍱 AI {cuisine} Food Menu for {goal}")

if st.button("✨ Generate AI Food Menu"):
    with st.spinner("Cura AI is preparing your personalized food menu..."):
        # The prompt remains professional but the UI labels are now "Food Menu"
        prompt = f"""
        Act as a Nutritionist. Create a 1-day {cuisine} food menu for a {g}, {a}yrs, {w}kg. 
        Goal: {goal}. Medical Context: {meds}. Vitals: BP {bp}, HR {hr}.
        Target: {tdee} calories. 
        Provide: Breakfast, Lunch, Dinner, and a Snack. 
        Briefly explain why this menu fits the goal: {goal}.
        """

        try:
            # Attempt 1: Standard Stable Model
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.success("✅ Food Menu Generated!")
                st.link_button("Order Ingredients on Zomato", f"https://www.zomato.com/search?q=healthy+{cuisine}")

        except Exception as e:
            error_str = str(e)
            # This is the Auto-Recovery if the 404 error happens again
            if "404" in error_str:
                try:
                    # Scan for any model your API key currently supports
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    # Pick the first 'flash' or 'pro' model found
                    fallback_name = models[0] 
                    
                    model_alt = genai.GenerativeModel(fallback_name)
                    response_alt = model_alt.generate_content(prompt)
                    
                    st.markdown(response_alt.text)
                    st.success(f"✅ Food Menu Generated (via {fallback_name})")
                except Exception as final_err:
                    st.error("🚨 Connection Error. Please verify your API Key in Streamlit Secrets.")
            else:
                st.error(f"Technical Issue: {error_str}")

# --- SIDEBAR RESTART ---
if st.sidebar.button("🔄 Restart Profile"):
    st.session_state.clear()
    st.switch_page("cura.py")

st.divider()
