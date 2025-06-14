import streamlit as st
import pandas as pd

st.set_page_config(page_title="9ineHealth Dashboard", layout="wide")

st.title("🩺 9ineHealth Live Dashboard")
st.markdown("**Visuals from triage, dispatch, access logs and CO₂ tracker**")

try:
    triage_stats = pd.read_csv("triage_stats.csv")
    st.success(f"✅ Loaded triage_stats.csv with {triage_stats.shape[0]} rows")
    st.dataframe(triage_stats)

    dispatch_logs = pd.read_csv("dispatch_logs.csv")
    st.success(f"✅ Loaded dispatch_logs.csv with {dispatch_logs.shape[0]} rows")
    st.dataframe(dispatch_logs)

    blockchain_logs = pd.read_csv("blockchain_logs.csv")
    st.success(f"✅ Loaded blockchain_logs.csv with {blockchain_logs.shape[0]} rows")
    st.dataframe(blockchain_logs)

    co2_savings = pd.read_csv("co2_savings.csv")
    st.success(f"✅ Loaded co2_savings.csv with {co2_savings.shape[0]} rows")
    st.line_chart(co2_savings.set_index("Date"))
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
