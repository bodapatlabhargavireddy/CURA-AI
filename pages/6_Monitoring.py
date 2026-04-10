
import streamlit as st
import google.generativeai as genai
import time

# --- CONFIG ---
st.set_page_config(page_title="Cura Monitoring", layout="wide")

# --- DATA RETRIEVAL ---
# Get height from session state (needed for BMI)
height_cm = st.session_state.get("height", 170.0) 
starting_weight = st.session_state.get("weight", 70.0)
goal = st.session_state.get("goal", "Maintenance")

st.title("🛡️ Cura Live Monitoring")

# --- DYNAMIC WEIGHT & BMI ---
st.subheader("⚖️ Real-Time Body Metrics")
w_col1, w_col2, w_col3 = st.columns(3)

with w_col1:
    # Use a unique key for this page's input
    current_weight = st.number_input("Enter Current Weight (kg)", 30.0, 200.0, float(starting_weight))

with w_col2:
    # FIXED BMI MATH: Uses 'current_weight' instead of 'starting_weight'
    bmi = round(current_weight / ((height_cm / 100) ** 2), 1)
    
    # Determine color/status
    if bmi < 18.5: status, color = "Underweight", "blue"
    elif 18.5 <= bmi < 25: status, color = "Healthy", "green"
    elif 25 <= bmi < 30: status, color = "Overweight", "orange"
    else: status, color = "Obese", "red"
    
    st.metric("Live BMI", f"{bmi}", delta=status, delta_color="normal")
    st.markdown(f"Status: :{color}[**{status}**]")

with w_col3:
    weight_diff = round(current_weight - starting_weight, 2)
    st.metric("Weight Change", f"{weight_diff} kg", delta=weight_diff, delta_color="inverse")

# --- UPDATE GLOBAL DATA ---
if st.button("💾 Sync Data to Dashboard"):
    st.session_state["weight"] = current_weight
    st.success("Weight and BMI synced! Check your Dashboard page now.")

st.divider()

# --- THE AI PROMPT (Now with Live BMI) ---
import streamlit as st
import google.generativeai as genai
import time

# --- AI GENERATOR BLOCK (REPLACE YOURS WITH THIS) ---
if st.button("🍴 Generate Menu Based on NEW BMI"):
    with st.spinner("AI analyzing your profile..."):
        # 1. Models to try (Newest 2026 models first)
        # Gemini 3.1 Flash-Lite is the most 'available' for free tier right now
        models_to_try = [
            'models/gemini-3.1-flash-lite-preview', 
            'models/gemini-3.1-flash-preview',
            'models/gemini-2.5-flash'
        ]
        
        prompt = f"""
        Act as a Dietician. 
        User Height: {height_cm}cm, Current Weight: {current_weight}kg.
        Calculated BMI: {bmi} ({status}). Goal: {goal}.
        
        Task: Provide a 1-day menu for an '{status}' profile to reach '{goal}'. 
        Format: Use bold headers, be very concise to save tokens.
        """
        
        success = False
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            for model_id in models_to_try:
                try:
                    model = genai.GenerativeModel(model_id)
                    # Use a short timeout to keep the demo moving
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.markdown(response.text)
                        st.balloons()
                        success = True
                        break # Success! Stop trying other models.
                
                except Exception as e:
                    # If it's a 429 (Busy) or 404 (Old Model), try the next one
                    if "429" in str(e) or "404" in str(e):
                        continue 
                    else:
                        st.error(f"Error with {model_id}: {e}")
            
            if not success:
                st.error("🚨 All AI Engines are currently at capacity. Please wait 20 seconds.")
                
        except Exception as config_err:
            st.error(f"Configuration Error: {config_err}")
