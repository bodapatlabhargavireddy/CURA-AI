import streamlit as st
import google.generativeai as genai

# --- 1. SYNC & DATA ---
# Ensures 60kg is pulled correctly from your first page (cura.py)
w = st.session_state.get("weight", 60.0) 
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Female")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# Calculate metrics locally (Fast & Reliable)
bmi = round(w / ((h/100)**2), 1)
bmr = (10 * w) + (6.25 * h) - (5 * a) + (5 if g == "Male" else -161)
cal = int(bmr * 1.55) # Assuming Moderate Activity
prot = int(w * 1.8)

# --- 2. THE AI LOGIC WITH DYNAMIC MODEL CHECK ---
if "ai_output" not in st.session_state:
    st.session_state.ai_output = None

if st.button("🚀 Generate Schedule & Menu"):
    if st.session_state.ai_output:
        st.success("✅ Loading existing plan...")
    else:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # --- FIX FOR 404: FIND VALID MODEL ---
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = models[0] if models else "gemini-1.5-flash"
            
            model = genai.GenerativeModel(target_model)
            prompt = f"Create a 1-day {cuisine} meal schedule for a {w}kg {g}. Goal: {goal}. Target: {cal}kcal."
            
            response = model.generate_content(prompt)
            st.session_state.ai_output = response.text
            st.balloons()
            
        except Exception as e:
            # --- FIX FOR 429: LOCAL BACKUP ---
            st.warning("⚠️ Cloud Engine busy. Using Local Expert Engine...")
            st.session_state.ai_output = f"""
            ### 🍱 {cuisine} Schedule for {w}kg {g}
            * **08:30 AM (Breakfast):** Vegetable Poha or Sprouts (High Fiber)
            * **01:30 PM (Lunch):** {cuisine} Thali - Brown Rice, Dal, Veggies
            * **05:00 PM (Workout):** 45 mins Activity + Protein Snack
            * **08:30 PM (Dinner):** Light Soup & Grilled Paneer/Chicken
            
            **Daily Targets:** {cal} kcal | {prot}g Protein
            *💡 Backup mode active: Stats synced for {w}kg.*
            """

# Display the output (from AI or Backup)
if st.session_state.ai_output:
    st.markdown("---")
    st.markdown(st.session_state.ai_output)
