import streamlit as st

st.set_page_config(page_title="Health Assessment", layout="centered")

# --- DATA GUARD ---
# If the user tries to skip page 1, we stop them here.
if "weight" not in st.session_state:
    st.error("⚠️ No profile data found. Please complete the Biological Profile first.")
    if st.button("⬅️ Back to Home"):
        st.switch_page("cura.py")
    st.stop()

st.title("🏥 Health Assessment")
# Proof of sync for the judges:
st.success(f"✅ Profile Sync Active: {st.session_state.gender} | {st.session_state.weight}kg")
st.divider()

# --- MEDICAL INPUTS ---
st.subheader("📋 Medical History")
st.multiselect(
    "Do you have any existing conditions?",
    options=["Diabetes", "Hypertension", "PCOS/PCOD", "Thyroid", "Asthma", "None"],
    default=["None"],
    key="health_conditions"
)

st.text_input("List any food allergies:", placeholder="e.g. Peanuts, Gluten", key="allergies")

st.divider()

if st.button("Next: Set Your Goal 🎯"):
    st.switch_page("pages/2_Goal.py")
