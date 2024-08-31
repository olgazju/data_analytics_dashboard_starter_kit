import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import requests

st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize connection to PostgreSQL
conn = st.connection("postgresql", type="sql")


# Helper function to format large numbers
def format_large_number(number):
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return f"{number:.2f}"


# Function to fetch metrics data from CoinGecko API
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def fetch_coin_data(coin_id, api_key):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    headers = {
        "x-cg-demo-api-key": api_key
    }
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }
    response = requests.get(url, headers=headers, params=params, timeout=300)
    if response.status_code == 200:
        data = response.json()
        current_price = data['market_data']['current_price']['usd']
        market_cap = data['market_data']['market_cap']['usd']
        high_24h = data['market_data']['high_24h']['usd']
        low_24h = data['market_data']['low_24h']['usd']
        price_change_24h = data['market_data']['price_change_percentage_24h']

        # Determine arrow direction and color for price change
        arrow = "⬆️" if price_change_24h > 0 else "⬇️"
        color = "green" if price_change_24h > 0 else "red"

        metrics = {
            "Current Price": f"${current_price:,.2f}",
            "Market Cap": f"${format_large_number(market_cap)}",
            "24h High": f"${high_24h:,.2f}",
            "24h Low": f"${low_24h:,.2f}",
            "24h Price Change": f"<span style='color:{color};'>{arrow} {price_change_24h:.2f}%</span>"
        }
        return metrics
    else:
        # Return default values if API call fails
        return {
            "Current Price": "$0",
            "Market Cap": "$0",
            "24h High": "$0",
            "24h Low": "$0",
            "24h Price Change": "0%"
        }


# Get API key from secrets
api_key = st.secrets["token"]["coin_token"]


@st.cache_data(show_spinner=False)
def get_ohlc_data(coin):
    query = f"SELECT * FROM ohlc_data WHERE coin_id = '{coin}'"
    return conn.query(query)


@st.cache_data(show_spinner=False)
def get_coins():
    coin_query = "SELECT DISTINCT coin_id FROM ohlc_data"
    result = conn.query(coin_query)
    return result['coin_id'].tolist()


# Load available coins and allow the user to select one
coins = get_coins()
coin = st.sidebar.selectbox("Select Cryptocurrency", coins)

# Load OHLC data for the selected coin
ohlc_df = get_ohlc_data(coin)

# Fetch metrics for the selected coin
metrics = fetch_coin_data(coin, api_key)

# Get minimum and maximum dates from the dataframe
min_date = ohlc_df['date'].min()
max_date = ohlc_df['date'].max()

# Sidebar date filters using the min and max dates from the data
start_date = st.sidebar.date_input("From:", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("To:", value=max_date, min_value=min_date, max_value=max_date)

# Filter the dataframe based on the selected dates
filtered_df = ohlc_df[(ohlc_df['date'] >= pd.to_datetime(start_date)) & (ohlc_df['date'] <= pd.to_datetime(end_date))]

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
metrics_col1, metrics_col2, metrics_col3, metrics_col4, metrics_col5 = st.columns(5)

with metrics_col1:
    st.markdown("<div class='metric-box'>Current Price<br><b>{}</b></div>".format(metrics["Current Price"]), unsafe_allow_html=True)

with metrics_col2:
    st.markdown("<div class='metric-box'>Market Cap<br><b>{}</b></div>".format(metrics["Market Cap"]), unsafe_allow_html=True)

with metrics_col3:
    st.markdown("<div class='metric-box'>24h High<br><b>{}</b></div>".format(metrics["24h High"]), unsafe_allow_html=True)

with metrics_col4:
    st.markdown("<div class='metric-box'>24h Low<br><b>{}</b></div>".format(metrics["24h Low"]), unsafe_allow_html=True)

with metrics_col5:
    st.markdown("<div class='metric-box'>24h Price Change<br><b>{}</b></div>".format(metrics["24h Price Change"]), unsafe_allow_html=True)

# Central Candlestick Chart
fig = go.Figure(data=[go.Candlestick(x=filtered_df['date'],
                                     open=filtered_df['open'],
                                     high=filtered_df['high'],
                                     low=filtered_df['low'],
                                     close=filtered_df['close'],
                                     increasing_line_color='green',
                                     decreasing_line_color='red')])

fig.update_layout(
    title="OHLC Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
)
st.plotly_chart(fig, use_container_width=True)
