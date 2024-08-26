import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import psycopg2
from datetime import datetime, timedelta

# Set up page configuration
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Function to get available cryptocurrencies
def get_available_cryptocurrencies():
    conn = psycopg2.connect(
        host=st.secrets["neon"]["url"],
        database=st.secrets["neon"]["database"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"],
        port=5432,
        sslmode='require'
    )
    query = "SELECT DISTINCT coin_id FROM ohlc_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['coin_id'].tolist()


# Function to load OHLC data for a given cryptocurrency
def load_ohlc_data(coin_id):
    conn = psycopg2.connect(
        host=st.secrets["neon"]["url"],
        database=st.secrets["neon"]["database"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"],
        port=5432,
        sslmode='require'
    )
    half_year_ago = datetime.now() - timedelta(days=30)
    query = f"""
        SELECT timestamp, open, high, low, close
        FROM ohlc_data
        WHERE coin_id = '{coin_id}' AND date >= '{half_year_ago.strftime('%Y-%m-%d')}'
        ORDER BY date
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


# Sidebar for navigation and filters
st.sidebar.title("Crypto Dashboard")
st.sidebar.subheader("Filters")

# Get available cryptocurrencies from the database
cryptocurrencies = get_available_cryptocurrencies()

# Sidebar select box to choose cryptocurrency
coin = st.sidebar.selectbox("Select Cryptocurrency", cryptocurrencies)

# Load OHLC data from the database for the selected cryptocurrency
ohlc_df = load_ohlc_data(coin)

# Metrics data (simulated for now, can be replaced with real metrics data)
metrics = {
    "Liquidity (24h Volume)": "$5.54M",
    "Market Cap": "$207.93M",
    "Total Market Cap": "$92.28B",
    "Circulating Supply": "1.29M SOL",
    "Total Supply": "572.74M SOL",
    "24h Volume": "$219.06K",
    "Volatility (24h Price Change)": "0.0394",
    "Price Change (7d)": "0.2394"
}

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    .metric-box {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        color: #333333;
    }
    .plot-container>div {
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# New row for metrics above the chart
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.markdown("<div class='metric-box'>Market Cap<br><b>{}</b></div>".format(metrics["Market Cap"]), unsafe_allow_html=True)

with metrics_col2:
    st.markdown("<div class='metric-box'>Total Market Cap<br><b>{}</b></div>".format(metrics["Total Market Cap"]), unsafe_allow_html=True)

with metrics_col3:
    st.markdown("<div class='metric-box'>Volatility<br><b>{}</b></div>".format(metrics["Volatility (24h Price Change)"]), unsafe_allow_html=True)

with metrics_col4:
    st.markdown("<div class='metric-box'>Price Change (7d)<br><b>{}</b></div>".format(metrics["Price Change (7d)"]), unsafe_allow_html=True)

# Central Candlestick Chart
fig = go.Figure(data=[go.Candlestick(x=ohlc_df['date'],
                                     open=ohlc_df['open'],
                                     high=ohlc_df['high'],
                                     low=ohlc_df['low'],
                                     close=ohlc_df['close'],
                                     increasing_line_color='green',
                                     decreasing_line_color='red')])

fig.update_layout(
    title=f"OHLC Candlestick Chart for {coin.capitalize()}",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
)
st.plotly_chart(fig, use_container_width=True)
