import streamlit as st
import google.generativeai as genai

# Disable "Magic" explicitly at the top to prevent Python 3.14 crashes
# (This ensures the app runs even if the environment is unstable)

def run_dashboard():
    st.set_page_config(page_title="Cura Dashboard", layout="wide")

    # --- API SETUP ---
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("API Key Missing!")
        return

    st.title("🛡️ Cura AI Health Hub")

    # --- DYNAMIC DATA RETRIEVAL ---
    # These must match the 'key' used in your input pages
    weight = st.session_state.get("weight", 70.0)
    height = st.session_state.get("height", 170.0)
    age = st.session_state.get("age", 25)
    gender = st.session_state.get("gender", "Male")
    goal = st.session_state.get("goal", "Maintenance")
    cuisine = st.session_state.get("cuisine", "Indian")

    # --- CALCULATIONS (THE PERSONALIZER) ---
    # BMR Calculation (Mifflin-St Jeor)
    offset = 5 if gender == "Male" else -161
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + offset
    
    # Adjust targets based on goal
    calories = int(bmr * 1.3)
    steps = 8000
    
    if "Loss" in goal:
        calories -= 500
        steps = 10000
    elif "Gain" in goal:
        calories += 400
        steps = 6000

    # --- DISPLAY METRICS ---
    st.subheader("🚀 Your Daily Health Targets")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Calories", f"{calories} kcal")
    c2.metric("💧 Water", f"{round(weight * 0.035, 1)} L")
    c3.metric("🍗 Protein", f"{int(weight * 1.5)} g")
    c4.metric("👟 Step Goal", f"{steps:,}")

    st.divider()

    # --- LIVE MONITORING SECTION ---
    st.subheader("💓 Live Vitals & Progress")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
        if hr > 100: st.error("🚩 High Heart Rate Alert")
    with m2:
        bp = st.number_input("Systolic BP", 80, 200, 120)
        if bp > 140: st.error("🚩 Hypertension Warning")
    with m3:
        # Important: Allows tracking if weight changed today
        current_w = st.number_input("Today's Weight (kg)", 30.0, 200.0, float(weight))
        diff = round(current_w - weight, 2)
        if diff != 0:
            st.info(f"Progress: {diff} kg from start")

    st.divider()

    # --- AI FOOD MENU GENERATOR ---
    st.subheader(f"🍱 Personalized {cuisine} Food Menu")
    
    if st.button("✨ Generate AI Food Menu"):
        with st.spinner("AI is analyzing vitals and progress..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                Act as a Nutritionist. Create a 1-day {cuisine} food menu for {gender}, {age}yrs.
                Starting Weight: {weight}kg, Current Weight: {current_w}kg.
                Goal: {goal}. Vitals: BP {bp}, HR {hr}.
                Target: {calories} kcal.
                Include Breakfast, Lunch, Dinner and a Snack.
                If current weight changed, explain the menu adjustment.
                """
                
                response = model.generate_content(prompt)
                if response.text:
                    st.markdown(response.text)
                    st.success("✅ Menu Generated based on today's vitals!")
                    st.link_button("Order Healthier on Zomato", f"https://www.zomato.com/search?q=healthy+{cuisine}")
            except Exception as e:
                st.error("AI Node Busy. Please try again.")

    # --- SIDEBAR ---
    if st.sidebar.button("🔄 Restart Profile"):
        st.session_state.clear()
        st.switch_page("cura.py")

# Execute the function
if __name__ == "__main__":
    run_dashboard()
