import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="9ineHealth Dashboard", layout="wide")

st.title("🩺 9ineHealth Live Dashboard")
st.caption("Visuals from triage, dispatch, access logs and CO₂ tracker")

# === Load data ===
try:
    triage_stats = pd.read_csv("triage_stats.csv")
    dispatch_logs = pd.read_csv("dispatch_logs.csv")
    co2_savings = pd.read_csv("co2_savings.csv")
    blockchain_logs = pd.read_csv("blockchain_logs.csv")
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

# === Triage Chart ===
st.subheader("📊 Triage Statistics")
triage_chart = alt.Chart(triage_stats).mark_bar().encode(
    x="Condition:N",
    y="Count:Q",
    color="Condition:N"
)
st.altair_chart(triage_chart, use_container_width=True)

# === Dispatch Log Table ===
st.subheader("🚑 Recent Dispatch Logs")
st.dataframe(dispatch_logs)

# === Blockchain Log Table ===
st.subheader("🔐 Blockchain Access Logs")
st.dataframe(blockchain_logs)

# === CO₂ Savings Chart ===
st.subheader("🌱 Estimated CO₂ Emissions Avoided")
co2_chart = alt.Chart(co2_savings).mark_line(point=True).encode(
    x="Date:T",
    y="CO2_Saved:Q"
)
st.altair_chart(co2_chart, use_container_width=True)
