import streamlit as st

st.set_page_config(page_title="Health Assessment", layout="centered")

# --- 1. DATA PERSISTENCE CHECK ---
# We check the session_state for the 'weight' key from the home page.
# If it's missing, we provide a clean way to go back.
if "weight" not in st.session_state or st.session_state.weight == 0:
    st.error("⚠️ No profile data found. Please complete the Biological Profile first.")
    if st.button("⬅️ Back to Home"):
        st.switch_page("cura.py")
    st.stop()  # Stops the rest of the code from running until data is present

# --- 2. DISPLAY CONFIRMED DATA ---
st.title("🏥 Health Assessment")
st.success(f"✅ Profile Sync Active: {st.session_state.gender} | {st.session_state.age} yrs | {st.session_state.weight}kg")
st.write("Now, let's define your medical context to ensure AI safety.")
st.divider()

# --- 3. HEALTH INPUTS ---
st.subheader("📋 Medical History")

# Using multiselect for flexibility
conditions = st.multiselect(
    "Do you have any existing conditions?",
    options=["Diabetes", "Hypertension", "PCOS/PCOD", "Thyroid", "Asthma", "None"],
    default="None",
    key="health_conditions" # This key stores the choice for the Dashboard
)

# Text input for allergies
st.text_input(
    "List any food allergies:", 
    placeholder="e.g. Peanuts, Gluten, Dairy", 
    key="allergies" # This key stores the text for the Dashboard
)

st.divider()

# --- 4. NAVIGATION ---
if st.button("Next: Set Your Goal 🎯"):
    # Optional: Logic to prevent moving forward if nothing is selected
    if not conditions:
        st.warning("Please select a condition or 'None' to continue.")
    else:
        st.switch_page("pages/2_🎯_Goal.py")
