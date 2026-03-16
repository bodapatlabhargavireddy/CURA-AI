import streamlit as st

st.title("📈 Journey Monitoring")
current_w = st.number_input("Update Weight (kg)", value=float(st.session_state.get("weight", 70)))
diff = round(current_w - st.session_state.get("weight", 70), 2)

if diff < 0:
    st.balloons()
    st.success(f"Down {abs(diff)}kg! Awesome work.")
elif diff > 0:
    st.warning(f"Up {diff}kg. Let's increase activity today!")
