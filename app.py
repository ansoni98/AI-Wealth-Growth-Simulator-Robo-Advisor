import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(page_title="AI Wealth Growth Simulator", layout="wide")

# ---------- Clean Premium Styling ----------
st.markdown("""
<style>
.main {background-color:#0f172a; color:white;}
.block-container {padding-top:1rem;}
.metric-card {background:#111827; padding:12px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.title("💰 AI Wealth Growth Simulator + Robo Advisor")

# ---------- Sidebar ----------
st.sidebar.header("Inputs")
P = st.sidebar.number_input("Investment Amount (₹)", value=10000)
T = st.sidebar.slider("Time Period (Years)", 1, 30, 10)
risk = st.sidebar.selectbox("Risk Level", ["Low", "Medium", "High"])
goal = st.sidebar.number_input("🎯 Target Goal (₹)", value=100000)
tax_rate = st.sidebar.slider("Tax Rate (%)", 0, 30, 10)/100

rates = {"Low":0.05, "Medium":0.10, "High":0.15}

# ---------- Growth ----------
def growth(P,r,T):
    return [P*(1+r)**t for t in range(T+1)]

values = growth(P,rates[risk],T)

# ---------- KPI ----------
st.subheader("📊 Overview")
col1,col2,col3 = st.columns(3)
final_val = values[-1]
col1.metric("Final Value", f"₹{int(final_val)}")
col2.metric("Profit", f"₹{int(final_val-P)}")
col3.metric("Growth %", f"{int((final_val/P-1)*100)}%")

# ---------- Growth Chart ----------
st.subheader("📈 Growth Trend")
fig = go.Figure()
fig.add_trace(go.Scatter(y=values, mode='lines', line=dict(width=3)))
fig.update_layout(template="plotly_dark", margin=dict(l=20,r=20,t=20,b=20))
st.plotly_chart(fig,use_container_width=True)

# ---------- Goal Planning ----------
st.subheader("🎯 Goal Planning")
if final_val>=goal:
    st.success("✅ Goal Achieved")
else:
    short = goal-final_val
    st.error(f"❌ Shortfall ₹{int(short)}")
    req = goal/((1+rates[risk])**T)
    st.info(f"💡 Required Investment: ₹{int(req)}")

if P>0 and goal>P:
    time_needed = math.log(goal/P)/math.log(1+rates[risk])
    st.write(f"⏳ Time to Goal: {round(time_needed,1)} years")

# ---------- SIP ----------
st.subheader("🔄 Required SIP")
months = T*12
r = rates[risk]/12
sip = goal*r/((1+r)**months-1) if r>0 else goal/months
st.metric("Monthly SIP Needed", f"₹{int(sip)}")

# ---------- Portfolio ----------
st.subheader("💼 Portfolio Performance")
portfolio = pd.DataFrame({"Year":list(range(T+1)),"Value":values})
st.line_chart(portfolio.set_index("Year"))

# ---------- Monte Carlo ----------
st.subheader("🎲 Monte Carlo Simulation")
sims = []
for _ in range(40):
    val = P
    temp=[]
    for _ in range(T):
        rand = np.random.normal(rates[risk],0.05)
        val *= (1+rand)
        temp.append(val)
    sims.append(temp)

fig2 = go.Figure()
for s in sims:
    fig2.add_trace(go.Scatter(y=s,mode='lines',opacity=0.25))
fig2.update_layout(template="plotly_dark", margin=dict(l=20,r=20,t=20,b=20))
st.plotly_chart(fig2,use_container_width=True)

# ---------- Inflation + Tax ----------
st.subheader("📉 Real Returns")
inflation=0.06
real = final_val/((1+inflation)**T)
after_tax = final_val*(1-tax_rate)
col1,col2 = st.columns(2)
col1.metric("After Inflation", f"₹{int(real)}")
col2.metric("After Tax", f"₹{int(after_tax)}")

# ---------- Comparison ----------
st.subheader("📊 Investment Comparison")
fd = P*(1.06)**T
mf = P*(1.12)**T
stocks = P*(1.15)**T
fig3 = go.Figure(data=[go.Bar(x=["FD","Mutual Fund","Stocks"], y=[fd,mf,stocks])])
fig3.update_layout(template="plotly_dark")
st.plotly_chart(fig3,use_container_width=True)

# ---------- Rebalancing ----------
st.subheader("🔄 Rebalancing Suggestion")
if T>5:
    st.info("Reduce equity gradually, increase bonds")
else:
    st.info("Focus on growth assets")

# ---------- AI Advisor ----------
st.subheader("🤖 AI Investment Advisor")
q = st.text_input("Ask your investment question:")
if q:
    if "risk" in q.lower():
        st.write("Choose risk based on time horizon")
    elif "sip" in q.lower():
        st.write("SIP ensures disciplined investing")
    else:
        st.write("Diversify and invest long-term")

# ---------- Download ----------
st.subheader("📥 Download Report")
report = f"Investment: {P}\nFinal Value: {int(final_val)}\nGoal: {goal}"
st.download_button("Download Summary", report)

st.markdown("---")
st.caption("AI Wealth Simulator | Clean Premium UI")
