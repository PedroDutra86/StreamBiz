import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache_data
def load_data(company):
  action_data = yf.Ticker(company)
  action_prices = action_data.history(period="1d", start="2010-01-01",end="2025-01-01")
  action_prices = action_prices[["Close"]]
  return action_prices

data = load_data("ITUB4.SA")

st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos
""")

st.line_chart(data)