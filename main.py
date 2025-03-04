import streamlit as st
import pandas as pd
import yfinance as yf

# Fetches and returns the daily closing stock prices for the given company from 2010 to 2025
@st.cache_data
def load_data(companies):
  tickers_text = " ".join(companies)
  stocks_data = yf.Tickers(tickers_text)
  stocks_prices = stocks_data.history(period="1d", start="2010-01-01",end="2025-01-01")
  stocks_prices = stocks_prices["Close"]
  return stocks_prices


stocks = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]

# Defining variables for the function to search for the stock ticker on Yahoo Finance
data = load_data(stocks)

#Streamlit Graphical Interface
st.write("""
# Stock Price App
The chart below shows the evolution of stock prices over the years.
""")

selected_stocks = st.multiselect("Choose the stocks to visualize",data.columns)
if selected_stocks:
  data = data[selected_stocks]
  if len(selected_stocks) == 1:
    single_stock = selected_stocks[0]
    data = data.rename(columns={single_stock: "Close"})

st.line_chart(data)