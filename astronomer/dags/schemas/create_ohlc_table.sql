CREATE TABLE IF NOT EXISTS ohlc_data (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    timestamp BIGINT,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    date TIMESTAMP,
    UNIQUE (coin_id, timestamp)
);
