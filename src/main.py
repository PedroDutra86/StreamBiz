# Importando bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
# Funções de carregamento de dados

@st.cache_data
def load_data(companies):
    end_date = datetime.today()
    tickers_text = " ".join(companies)
    stocks_data = yf.Tickers(tickers_text)
    stock_prices = stocks_data.history(period="1d", start="2010-01-01", end=end_date)
    stock_prices = stock_prices["Close"]
    return stock_prices

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "IBOV.csv"))
@st.cache_data
def load_stock_tickers():
    base_tickers = pd.read_csv(file_path, sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

# Carregar os tickers e os dados das ações
stocks = load_stock_tickers()
data = load_data(stocks)

# Interface do Streamlit
st.write("""
# Stock Price App
The chart below shows the evolution of stock prices over the years.
""") 

# Filtros de visualização
st.sidebar.header("Filters")

# Filtro de ações
selected_stocks = st.sidebar.multiselect("Choose the stocks to visualize", data.columns)
if selected_stocks:
    data = data[selected_stocks]
    if len(selected_stocks) == 1:
        single_stock = selected_stocks[0]
        data = data.rename(columns={single_stock: "Close"})

# Filtro de datas - Intervalo inicial menor (1 mês, por exemplo)
start_date = data.index.min().to_pydatetime()
end_date = data.index.max().to_pydatetime()

# Inicializando o intervalo de datas com 1 mês de diferença
initial_date_range = (end_date, end_date - timedelta(days=365))

# Filtro de datas no slider
date_range = st.sidebar.slider("Select the period", 
                              min_value=start_date, 
                              max_value=end_date,
                              value=initial_date_range,
                              step=timedelta(days=1))

# Filtrando os dados com base no intervalo selecionado
data = data.loc[date_range[0]:date_range[1]]

# Criar o gráfico
st.line_chart(data)

# Cálculo de performance
performance_text = ""

if len(selected_stocks) == 0:
    selected_stocks = list(data.columns)
elif len(selected_stocks) == 1:
    data = data.rename(columns={"Close": single_stock})

# Inicializando a carteira com valores fixos para cada ação
portfolio = [1000 for stock in selected_stocks]
initial_portfolio_value = sum(portfolio)

for i, stock in enumerate(selected_stocks):
    stock_performance = data[stock].iloc[-1] / data[stock].iloc[0] - 1
    stock_performance = float(stock_performance)

    portfolio[i] = portfolio[i] * (1 + stock_performance)

    if stock_performance > 0:
        performance_text = performance_text + f"  \n{stock}: :green[{stock_performance:.1%}]"
    elif stock_performance < 0:
        performance_text = performance_text + f"  \n{stock}: :red[{stock_performance:.1%}]"
    else:
        performance_text = performance_text + f"  \n{stock}: {stock_performance:.1%}"

final_portfolio_value = sum(portfolio)
portfolio_performance = final_portfolio_value / initial_portfolio_value - 1

if portfolio_performance > 0:
    portfolio_performance_text = f"Portfolio performance with all assets: :green[{portfolio_performance:.1%}]"
elif portfolio_performance < 0:
    portfolio_performance_text = f"Portfolio performance with all assets: :red[{portfolio_performance:.1%}]"
else:
    portfolio_performance_text = f"Portfolio performance with all assets: {portfolio_performance:.1%}"

# Exibir as informações de performance
st.write(f"""
### Stock Performance
This is the performance of each stock in the selected period:

{performance_text}

{portfolio_performance_text}
""")
