
import streamlit as st
import google.generativeai as genai

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
if st.button("🍴 Generate Menu Based on NEW BMI"):
    with st.spinner("AI analyzing your new BMI..."):
        prompt = f"""
        Act as a Dietician. 
        User Height: {height_cm}cm, Current Weight: {current_weight}kg.
        Calculated BMI: {bmi} ({status}).
        Goal: {goal}.
        
        Task: Provide a 1-day menu specifically for an '{status}' BMI profile to reach '{goal}'.
        """
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error("AI is busy, but your BMI is updated above!")

# Navigation
if st.sidebar.button("🔄 Back to Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
