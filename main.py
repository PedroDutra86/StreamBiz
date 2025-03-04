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

st.sidebar.header('Filters')
#Stock Filter
selected_stocks = st.sidebar.multiselect("Choose the stocks to visualize",data.columns)
if selected_stocks:
  data = data[selected_stocks]
  if len(selected_stocks) == 1:
    single_stock = selected_stocks[0]
    data = data.rename(columns={single_stock: "Close"})

#Date Filter
start_date = data.index.min().to_pydatetime()
end_date = data.index.max().to_pydatetime()
date_range = st.sidebar.slider("Select the period", min_value = start_date, max_value = end_date, value = (start_date, end_date))

data = data.loc[date_range[0]:date_range[1]]

st.line_chart(data)