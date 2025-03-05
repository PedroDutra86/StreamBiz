# Stream Biz

Stream Biz is an application built with Streamlit to analyze historical stock closing data since January 1st, 2010. The goal is to provide insights and interactive visualizations of the stock's behavior over time.

## Technologies Used

- **Streamlit**: Framework for creating interactive web applications.
- **Pandas**: Library for data manipulation and analysis.
- **yfinance**: Library for fetching historical stock market data.

## Features

- Interactive display of stock closing prices.
- Graphs that allow visualization of stock price trends over time.
- Sidebar filters to customize the analysis:
  - Selection of specific stocks.
  - Adjustable date range with a slider.
- Portfolio performance calculation:
  - Displays individual stock performance over the selected period.
  - Calculates overall portfolio performance based on an initial fixed investment.

## How to Run the Project

```bash
   git clone https://github.com/your-username/stream-biz.git
   cd stream-biz
   pip install -r requirements.txt
   streamlit run app.py
```

