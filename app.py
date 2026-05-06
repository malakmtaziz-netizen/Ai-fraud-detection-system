import streamlit as st
import pandas as pd
import plotly.express as px
from data_manager import generate_sample_data
from fraud_logic import FraudEngine

# --- Page Setup ---
st.set_page_config(page_title="AI Financial Auditor", layout="wide", page_icon="🛡️")

# Custom CSS for a dark, professional aesthetic
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { border: 1px solid #333; padding: 15px; border-radius: 10px; background: #161b22; }
    .css-1kyx7g3 { background-color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Algorithmic Financial Auditor")
st.subheader("Automated Fraud Detection & AML Surveillance System")
st.divider()

# --- Data Initialization ---
if 'txn_data' not in st.session_state:
    raw_data = generate_sample_data(300)
    engine = FraudEngine()
    st.session_state.txn_data = engine.run_audit(raw_data)

df = st.session_state.txn_data

# --- Sidebar Controls ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=100)
st.sidebar.header("Audit Parameters")
min_score = st.sidebar.slider("Minimum Risk Score to Highlight", 0, 100, 40)
selected_location = st.sidebar.multiselect("Region Scan", df['location'].unique(), default=df['location'].unique())

filtered_df = df[(df['risk_score'] >= min_score) & (df['location'].isin(selected_location))]

# --- KPI Dashboard ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Audited", f"{len(df)}")
with col2:
    critical_count = len(df[df['risk_level'] == 'CRITICAL'])
    st.metric("Critical Alerts", critical_count, delta=f"{critical_count/len(df)*100:.1f}%", delta_color="inverse")
with col3:
    st.metric("Total Volume", f"${df['amount'].sum():,.0f}")
with col4:
    st.metric("System Health", "Active", delta="100ms Latency")

st.write("---")

# --- Visual Analytics ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("#### Risk Distribution vs. Transaction Value")
    fig = px.scatter(
        filtered_df, 
        x="timestamp", 
        y="amount", 
        color="risk_level",
        size="risk_score",
        hover_data=['sender_id', 'risk_reasons'],
        color_discrete_map={"CRITICAL": "#ff4b4b", "ELEVATED": "#ffa500", "STABLE": "#00d4ff"},
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### Risk Level Share")
    pie_fig = px.pie(
        df, 
        names='risk_level', 
        hole=0.5,
        color='risk_level',
        color_discrete_map={"CRITICAL": "#ff4b4b", "ELEVATED": "#ffa500", "STABLE": "#00d4ff"},
        template="plotly_dark"
    )
    st.plotly_chart(pie_fig, use_container_width=True)

# --- Audit Logs ---
st.markdown("#### Detailed Forensic Audit Logs")

def style_risk(row):
    if row['risk_level'] == 'CRITICAL':
        return ['background-color: #4b0000'] * len(row)
    elif row['risk_level'] == 'ELEVATED':
        return ['background-color: #332200'] * len(row)
    return [''] * len(row)

st.dataframe(
    filtered_df.style.apply(style_risk, axis=1), 
    use_container_width=True,
    hide_index=True
)

# --- Presentation Demo Actions ---
st.divider()
d_col1, d_col2 = st.columns(2)
with d_col1:
    if st.button("🚀 Run Real-Time Batch Analysis"):
        with st.spinner('Scanning global ledgers...'):
            import time
            time.sleep(2)
            st.success("Analysis Complete: 4 new suspicious patterns detected.")
            st.toast("Forensic Report Generated!")

with d_col2:
    st.download_button(
        label="📥 Export Audit Report (CSV)",
        data=df.to_csv().encode('utf-8'),
        file_name='audit_report.csv',
        mime='text/csv',
    )