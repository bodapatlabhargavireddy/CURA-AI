import streamlit as st
from google import genai
import time
import random

# --- CONFIG ---
st.set_page_config(page_title="Cura Monitoring", layout="wide")

# --- API CONFIGURATION ---
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key missing or invalid! Check your st.secrets.")
    st.stop()

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
if st.button("🍴 Generate Menu Based on NEW BMI"):
    with st.spinner("AI analyzing your profile..."):
        
        # Consistent stable model selection matching your other pages
        models_to_try = [
            "gemini-3.1-flash-lite",   
            "gemini-3.1-flash",        
            "gemini-2.5-flash"         
        ]
        
        prompt = f"""
        Act as a Dietician. 
        User Height: {height_cm}cm, Current Weight: {current_weight}kg.
        Calculated BMI: {bmi} ({status}). Goal: {goal}.
        
        Task: Provide a 1-day menu for an '{status}' profile to reach '{goal}'. 
        Format: Use bold headers, be very concise to save tokens.
        """
        
        success = False
        
        for model_id in models_to_try:
            # Simple retry loop for 503 clusters or minor hiccups
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_id,
                        contents=prompt
                    )
                    
                    if response.text:
                        st.markdown(response.text)
                        st.balloons()
                        success = True
                        break # Success! Break inner loop
                        
                except Exception as e:
                    err_str = str(e)
                    if "503" in err_str:
                        wait = random.uniform(1.5, 3.5)
                        time.sleep(wait)
                        continue # Retry same model
                    elif "429" in err_str or "404" in err_str:
                        break # Skip inner loop to jump to the next model layout
            
            if success:
                break # Break outer loop since we got our meal plan

        if not success:
            st.error("🚨 All AI Engines are currently at capacity. Please wait 20 seconds.")
