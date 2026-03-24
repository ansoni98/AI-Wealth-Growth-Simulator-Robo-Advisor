import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="AI Wealth Simulator", layout="wide")

# ---------- UI Styling ----------
st.markdown("""
    <style>
    .main {background-color: #0e1117; color: white;}
    .stMetric {background-color: #1f2937; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("💰 AI Wealth Growth Simulator + Robo Advisor")

# ---------- Sidebar ----------
st.sidebar.header("Input Parameters")
P = st.sidebar.number_input("Investment Amount (₹)", value=10000)
T = st.sidebar.slider("Time Period (Years)", 1, 20, 5)
risk = st.sidebar.selectbox("Risk Level", ["Low", "Medium", "High"])

# ---------- Rates ----------
rates = {"Low": 0.05, "Medium": 0.10, "High": 0.15}
inflation = 0.06

# ---------- Growth Calculation ----------
def calculate_growth(P, r, T):
    values = []
    for t in range(T + 1):
        values.append(P * (1 + r) ** t)
    return values

low = calculate_growth(P, rates["Low"], T)
med = calculate_growth(P, rates["Medium"], T)
high = calculate_growth(P, rates["High"], T)

# ---------- KPI ----------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Final Value (Selected)", f"₹{int(calculate_growth(P, rates[risk], T)[-1])}")
col2.metric("Total Profit", f"₹{int(calculate_growth(P, rates[risk], T)[-1] - P)}")
col3.metric("Growth %", f"{int(((calculate_growth(P, rates[risk], T)[-1] / P) - 1) * 100)}%")

# ---------- Chart ----------
st.subheader("📈 Growth Comparison")
fig = go.Figure()
fig.add_trace(go.Scatter(y=low, mode='lines', name='Low'))
fig.add_trace(go.Scatter(y=med, mode='lines', name='Medium'))
fig.add_trace(go.Scatter(y=high, mode='lines', name='High'))
st.plotly_chart(fig, use_container_width=True)

# ---------- Inflation Adjusted ----------
st.subheader("📉 Inflation Adjusted Value")
real_value = calculate_growth(P, rates[risk] - inflation, T)[-1]
st.write(f"Real Value after inflation: ₹{int(real_value)}")

# ---------- Portfolio Strategy ----------
st.subheader("💼 Dynamic Portfolio Strategy")
portfolio_data = []
for year in range(1, T + 1):
    if year < T * 0.3:
        stocks, bonds, gold = 70, 20, 10
    elif year < T * 0.7:
        stocks, bonds, gold = 50, 30, 20
    else:
        stocks, bonds, gold = 30, 50, 20
    portfolio_data.append([year, stocks, bonds, gold])

df = pd.DataFrame(portfolio_data, columns=["Year", "Stocks", "Bonds", "Gold"])
st.dataframe(df)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['Year'], y=df['Stocks'], name='Stocks'))
fig2.add_trace(go.Scatter(x=df['Year'], y=df['Bonds'], name='Bonds'))
fig2.add_trace(go.Scatter(x=df['Year'], y=df['Gold'], name='Gold'))
st.plotly_chart(fig2, use_container_width=True)

# ---------- Insights ----------
st.subheader("🧠 AI Insights")
if T > 5:
    st.success("Long-term investing increases returns significantly.")
if risk == "High":
    st.warning("High risk gives higher return but more volatility.")
if P < 5000:
    st.info("Consider increasing investment for better growth.")

# ---------- Goal Analysis ----------
st.subheader("🎯 Goal Analysis")
goal = 100000
final_val = calculate_growth(P, rates[risk], T)[-1]
if final_val >= goal:
    st.success(f"You can achieve ₹{goal}")
else:
    st.error(f"You fall short by ₹{int(goal - final_val)}")

# ---------- SIP Mode ----------
st.subheader("🔄 SIP Calculator")
monthly = P / 12
sip_value = 0
for i in range(T * 12):
    sip_value = (sip_value + monthly) * (1 + rates[risk]/12)
st.write(f"Future Value (SIP): ₹{int(sip_value)}")

st.markdown("---")
st.caption("AI FinTech Project - Wealth Simulator with Robo Advisory")

