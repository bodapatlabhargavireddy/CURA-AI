import streamlit as st
import google.generativeai as genai

# Setup
st.set_page_config(page_title="Cura AI", page_icon="🛡️", layout="wide")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Please add 'GEMINI_API_KEY' to Streamlit Secrets.")

# SIDEBAR: Shared User Profile
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("Cura Profile")
    st.divider()
    
    # Store in session_state so other pages can access these values
    st.session_state.age = st.number_input("Age", 15, 95, 25)
    st.session_state.gender = st.selectbox("Gender", ["Male", "Female"])
    st.session_state.weight = st.number_input("Weight (kg)", 35, 180, 70)
    st.session_state.height = st.number_input("Height (cm)", 100, 250, 170)
    st.session_state.meds = st.multiselect("Medical Conditions", ["None", "Diabetes", "BP", "Thyroid", "PCOD"])
    st.session_state.goal = st.selectbox("Current Goal", ["Maintenance", "Weight Loss", "Weight Gain"])
    st.session_state.cuisine = st.selectbox("Preferred Diet", ["Indian", "Western", "Continental"])

# Define the Navigation
pages = {
    "Overview": [
        st.Page("pages/dashboard.py", title="Health Dashboard", icon="📊", default=True),
    ],
    "Cura Tools": [
        st.Page("pages/meal_planner.py", title="AI Meal Planner", icon="🥘"),
        st.Page("pages/scanner.py", title="Vision Scanner", icon="📸"),
        st.Page("pages/tracker.py", title="My Journey", icon="📈"),
    ]
}

pg = st.navigation(pages)
pg.run()
