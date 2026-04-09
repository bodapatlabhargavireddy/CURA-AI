import streamlit as st

st.set_page_config(page_title="Health Assessment", layout="centered")

# --- DATA CHECK ---
# Checking if weight exists to ensure they came from Page 1
if "weight" not in st.session_state:
    st.warning("Please enter your profile details on the home page first.")
    if st.button("Go to Home"):
        st.switch_page("cura.py")
else:
    st.title("🏥 Health Assessment")
    st.write(f"Logged as: **{st.session_state.gender}**, **{st.session_state.weight}kg**")
    st.divider()

    # --- HEALTH INPUTS ---
    st.subheader("Medical History")
    st.multiselect(
        "Do you have any existing conditions?",
        options=["Diabetes", "Hypertension", "PCOS/PCOD", "Thyroid", "Asthma", "None"],
        key="health_conditions"
    )

    st.text_input("List any food allergies:", placeholder="e.g. Peanuts, Gluten", key="allergies")

    st.divider()

    if st.button("Next: Set Your Goal 🎯"):
        st.switch_page("pages/2_🎯_Goal.py")
