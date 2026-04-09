import streamlit as st

st.set_page_config(page_title="Diet Preferences", layout="centered", page_icon="🥗")

# Data Guard
if "user_goal" not in st.session_state:
    st.error("⚠️ Please set your goal first.")
    st.switch_page("pages/2_Goal.py")
    st.stop()

st.title("🥗 Diet & Nutrition")
st.write(f"Tailoring nutrition for: **{st.session_state.user_goal}**")

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "Dietary Preference:",
        options=["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian"],
        key="diet_type_val"
    )

with col2:
    st.selectbox(
        "Cuisine Style:",
        options=["Indian", "Continental", "Mediterranean", "Western"],
        key="cuisine_val"
    )

st.multiselect(
    "Specific food dislikes or restrictions:",
    options=["Spicy Food", "Dairy", "Gluten", "Sugar", "Mushrooms", "Sea Food"],
    key="dislikes_val"
)

st.divider()

if st.button("Generate Performance Dashboard 📊"):
    # Final data lock
    st.session_state["user_diet"] = st.session_state.diet_type_val
    st.session_state["user_cuisine"] = st.session_state.cuisine_val
    st.session_state["user_dislikes"] = st.session_state.dislikes_val
    
    st.switch_page("pages/4_Dashboard.py")
