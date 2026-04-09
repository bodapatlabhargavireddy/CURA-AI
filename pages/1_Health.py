import streamlit as st

st.set_page_config(page_title="Health Assessment", layout="centered")

# --- 1. DATA CHECK ---
# Using .get() ensures we don't crash if 'weight' isn't initialized yet
if st.session_state.get("weight") is None:
    st.error("⚠️ No profile data found. Please complete the Biological Profile first.")
    if st.button("⬅️ Back to Home"):
        st.switch_page("cura.py")
    st.stop() 

# --- 2. DISPLAY CONFIRMED DATA ---
st.title("🏥 Health Assessment")
# Pulling the real-time data from Session State
u_gender = st.session_state.get("gender", "User")
u_age = st.session_state.get("age", "N/A")
u_weight = st.session_state.get("weight", "N/A")

st.success(f"✅ Profile Sync Active: {u_gender} | {u_age} yrs | {u_weight}kg")
st.write("Please define your medical context to ensure AI safety.")
st.divider()

# --- 3. HEALTH INPUTS ---
st.subheader("📋 Medical History")

# Multiselect for conditions
conditions = st.multiselect(
    "Do you have any existing conditions?",
    options=["Diabetes", "Hypertension", "PCOS/PCOD", "Thyroid", "Asthma", "None"],
    default=["None"], # Changed to a list to match multiselect format
    key="health_conditions" 
)

# Text input for allergies
st.text_input(
    "List any food allergies:", 
    placeholder="e.g. Peanuts, Gluten, Dairy", 
    key="allergies" 
)

st.divider()

# --- 4. NAVIGATION ---
if st.button("Next: Set Your Goal 🎯"):
    if not conditions:
        st.warning("Please select a condition or 'None' to continue.")
    else:
        # RECOMMENDATION: Rename your file to '2_Goal.py' to avoid symbol errors
        try:
            st.switch_page("pages/2_Goal.py")
        except:
            # Fallback in case you haven't renamed the file yet
            st.switch_page("pages/2_Goal.py")
