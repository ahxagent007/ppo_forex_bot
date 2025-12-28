import streamlit as st
import pandas as pd

df = pd.read_csv("live/trade_log.csv", names=["time","action","balance"])

st.title("PPO Forex Dashboard")
st.line_chart(df.balance)
st.metric("Trades", len(df))
