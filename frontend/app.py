import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Example OHLC data with both red and green sticks
ohlc_data = {
    'timestamp': [
        1693180800000, 1693267200000, 1693353600000, 1693440000000, 1693526400000,
        1693612800000, 1693699200000, 1693785600000, 1693872000000, 1693958400000,
        1694044800000, 1694131200000, 1694217600000, 1694304000000, 1694390400000,
        1694476800000, 1694563200000, 1694649600000, 1694736000000, 1694822400000
    ],
    'open': [
        210, 215, 220, 225, 230,
        235, 230, 240, 245, 250,
        255, 250, 260, 265, 270,
        275, 270, 275, 280, 285
    ],
    'high': [
        215, 220, 225, 230, 235,
        240, 235, 245, 250, 255,
        260, 255, 265, 270, 275,
        280, 275, 280, 285, 290
    ],
    'low': [
        205, 210, 215, 220, 225,
        230, 225, 235, 240, 245,
        250, 245, 255, 260, 265,
        270, 265, 270, 275, 280
    ],
    'close': [
        212, 217, 218, 223, 228,
        234, 228, 242, 243, 248,
        254, 248, 258, 263, 268,
        273, 268, 274, 278, 282
    ]
}

# Convert data to a DataFrame
ohlc_df = pd.DataFrame(ohlc_data)
ohlc_df['date'] = pd.to_datetime(ohlc_df['timestamp'], unit='ms')


# Imitated metrics data
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

# Sidebar for navigation and filters
st.sidebar.title("Crypto Dashboard")
st.sidebar.subheader("Filters")
coin = st.sidebar.selectbox("Select Cryptocurrency", ["Bitcoin", "Ethereum", "Solana"])

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
    title="OHLC Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
)
st.plotly_chart(fig, use_container_width=True)
