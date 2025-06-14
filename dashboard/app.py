import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="9ineHealth Dashboard", layout="wide")

st.title("🩺 9ineHealth Live Dashboard")
st.caption("Visuals from triage, dispatch, access logs and CO₂ tracker")

try:
    triage_data = pd.read_csv("dashboard/triage_stats.csv")
    dispatch_data = pd.read_csv("dashboard/dispatch_logs.csv")
    blockchain_data = pd.read_csv("dashboard/blockchain_logs.csv")
    co2_data = pd.read_csv("dashboard/co2_savings.csv")
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Triage Statistics")
    chart = alt.Chart(triage_data).mark_bar().encode(
        x="Condition",
        y="Count",
        tooltip=["Condition", "Count"]
    ).properties(width=400, height=300)
    st.altair_chart(chart)

with col2:
    st.subheader("🚑 Dispatch Logs")
    st.dataframe(dispatch_data)

st.subheader("🔐 Blockchain Access Logs")
st.dataframe(blockchain_data)

st.subheader("🌱 CO₂ Savings")
line_chart = alt.Chart(co2_data).mark_line().encode(
    x="Date:T",
    y="CO2_Saved:Q",
    tooltip=["Date", "CO2_Saved"]
).properties(width=800, height=300)
st.altair_chart(line_chart)
