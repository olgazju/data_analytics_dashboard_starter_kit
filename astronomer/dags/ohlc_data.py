from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
import requests
import pandas as pd
import os


@dag(
    start_date=datetime(2024, 8, 28),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "airflow", "retries": 1},
    tags=["crypto", "coingecko"],
)
def ohlc_combined_load():
    @task
    def fetch_ohlc_data(coin_id: str, api_key: str, days: int, vs_currency: str = 'usd') -> pd.DataFrame:
        base_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
        headers = {
            "x-cg-demo-api-key": api_key
        }
        params = {
            "vs_currency": vs_currency,
            "days": days
        }
        response = requests.get(base_url, headers=headers, params=params, timeout=300)
        if response.status_code == 200:
            data = response.json()
            ohlc_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            ohlc_df['coin_id'] = coin_id
            ohlc_df['date'] = pd.to_datetime(ohlc_df['timestamp'], unit='ms')
            return ohlc_df
        else:
            return pd.DataFrame()

    @task
    def prepare_sql_query(df: pd.DataFrame) -> str:
        if df.empty:
            return ""
        values = [
            f"('{row['coin_id']}', {row['timestamp']}, {row['open']}, {row['high']}, {row['low']}, {row['close']}, '{row['date']}')"
            for _, row in df.iterrows()
        ]
        values_str = ", ".join(values)
        return f"""
        INSERT INTO ohlc_data (coin_id, timestamp, open, high, low, close, date)
        VALUES {values_str}
        ON CONFLICT (coin_id, timestamp) DO NOTHING;
        """

    @task
    def insert_data_to_neon(sql_query: str):
        if sql_query:
            pg_hook = PostgresHook(postgres_conn_id='neon-kit')
            pg_hook.run(sql_query)

    coins = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'litecoin']
    days = Variable.get("ohlc_load_days", default_var=1, deserialize_json=True)
    api_key = os.getenv("COIN_TOKEN")

    combined_query = ""
    for coin in coins:
        ohlc_df = fetch_ohlc_data(coin, api_key, days)
        sql_query = prepare_sql_query(ohlc_df)
        combined_query += sql_query

    insert_data_to_neon(combined_query)


ohlc_combined_load()
