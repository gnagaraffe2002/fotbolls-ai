
import streamlit as st

st.set_page_config(
    page_title="Football AI Pro",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FOOTBALL AI PRO")
st.subheader("Your personal football analyst")

st.divider()

st.header("🔎 Match Analysis")

home = st.text_input("Home Team", "Arsenal")
away = st.text_input("Away Team", "Chelsea")

if st.button("ANALYZE MATCH"):
    st.success(f"Match selected: {home} vs {away}")
    st.info("Football AI prediction engine is coming soon!")

st.divider()

st.header("📊 Analysis Center")

st.write("⚽ Goal Predictor")
st.write("🚩 Corner Predictor")
st.write("🥅 Shot Predictor")
st.write("📈 Team Performance")
st.write("🤖 Match Prediction Engine")

st.divider()

st.caption("Football AI Pro | Version 1.0
