import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Connect to PostgreSQL using SQLAlchemy engine
db_url = st.secrets["neon"]["db_url"]
engine = create_engine(db_url)


@st.cache_data(show_spinner=False)
def get_ohlc_data(coin):
    query = f"SELECT * FROM ohlc_data WHERE coin_id = '{coin}'"
    return pd.read_sql(query, con=engine)


@st.cache_data(show_spinner=False)
def get_coins():
    coin_query = text("SELECT DISTINCT coin_id FROM ohlc_data")
    with engine.connect() as connection:
        result = connection.execute(coin_query)
        return [row[0] for row in result]


# Load available coins and allow the user to select one
coins = get_coins()
coin = st.sidebar.selectbox("Select Cryptocurrency", coins)

# Load OHLC data for the selected coin
ohlc_df = get_ohlc_data(coin)

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
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.markdown("<div class='metric-box'>Market Cap<br><b>{}</b></div>".format("$207.93M"), unsafe_allow_html=True)

with metrics_col2:
    st.markdown("<div class='metric-box'>Total Market Cap<br><b>{}</b></div>".format("$92.28B"), unsafe_allow_html=True)

with metrics_col3:
    st.markdown("<div class='metric-box'>Volatility<br><b>{}</b></div>".format("0.0394"), unsafe_allow_html=True)

with metrics_col4:
    st.markdown("<div class='metric-box'>Price Change (7d)<br><b>{}</b></div>".format("0.2394"), unsafe_allow_html=True)

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
