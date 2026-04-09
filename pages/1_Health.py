import streamlit as st

st.set_page_config(page_title="Health Assessment", layout="centered", page_icon="🏥")

# --- DATA RECOVERY ---
# We check the "user_weight" key we forced in cura.py
if "user_weight" not in st.session_state:
    st.error("⚠️ Profile data lost. Please complete the Biological Profile first.")
    if st.button("⬅️ Back to Home"):
        st.switch_page("cura.py")
    st.stop()

st.title("🏥 Health Assessment")
st.success(f"✅ Sync Active for: {st.session_state.user_gender} | {st.session_state.user_weight}kg")
st.divider()

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
    # Force sync medical data
    st.session_state["final_conditions"] = st.session_state.health_conditions
    st.session_state["final_allergies"] = st.session_state.allergies
    st.switch_page("pages/2_Goal.py")
