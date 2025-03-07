-- Certifique-se de que o banco existe
\c stockbroker;

CREATE TABLE IF NOT EXISTS client (
    CodClient BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    balance NUMERIC(10,2) NOT NULL CHECK (balance >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS asset (
    CodAsset BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    quantity BIGINT NOT NULL CHECK (quantity >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS asset_client (
    ticker VARCHAR(10) NOT NULL,
    CodClient BIGINT REFERENCES client(CodClient) ON DELETE CASCADE,
    quantity BIGINT NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (ticker, CodClient),
    FOREIGN KEY (ticker) REFERENCES asset(ticker)
);

CREATE TABLE IF NOT EXISTS transaction (
    CodTransaction BIGSERIAL PRIMARY KEY,
    CodClient BIGINT REFERENCES client(CodClient) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    quantity BIGINT NOT NULL CHECK (quantity > 0),
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    transaction_type VARCHAR(4) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES asset(ticker)
);

CREATE TABLE IF NOT EXISTS withdraw_history (
    CodWithdraw BIGSERIAL PRIMARY KEY,
    CodClient BIGINT REFERENCES client(CodClient) ON DELETE CASCADE,
    value NUMERIC(10,2) NOT NULL CHECK (value > 0),  
    transaction_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deposit_history (
    CodDeposit BIGSERIAL PRIMARY KEY,
    CodClient BIGINT REFERENCES client(CodClient) ON DELETE CASCADE,
    value NUMERIC(10,2) NOT NULL CHECK (value > 0),  
    transaction_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO asset (name, ticker, price, quantity) VALUES
    ('Apple Inc.', 'AAPL', 175.50, 50),
    ('Tesla Inc.', 'TSLA', 800.25, 30),
    ('Amazon.com Inc.', 'AMZN', 3200.75, 20),
    ('Microsoft Corp.', 'MSFT', 295.80, 40),
    ('NVIDIA Corp.', 'NVDA', 650.60, 25),
    ('Alphabet Inc. (Google)', 'GOOGL', 2750.40, 10),
    ('Meta Platforms Inc.', 'META', 360.90, 35),
    ('Netflix Inc.', 'NFLX', 510.75, 15),
    ('Berkshire Hathaway Inc.', 'BRK.B', 320.50, 12),
    ('Johnson & Johnson', 'JNJ', 165.30, 45),
    ('Gold ETF', 'GLD', 185.75, 100),
    ('Bitcoin Trust', 'GBTC', 43.20, 200),
    ('Ethereum Fund', 'ETHF', 3250.80, 50),
    ('Coca-Cola Co.', 'KO', 60.45, 75),
    ('PepsiCo Inc.', 'PEP', 180.30, 60),
    ('Walt Disney Co.', 'DIS', 145.25, 55),
    ('Intel Corp.', 'INTC', 48.90, 90),
    ('Advanced Micro Devices', 'AMD', 110.75, 70),
    ('Visa Inc.', 'V', 230.40, 30),
    ('Mastercard Inc.', 'MA', 385.10, 25),
    ('JPMorgan Chase & Co.', 'JPM', 170.20, 40),
    ('Bank of America', 'BAC', 42.75, 100),
    ('ExxonMobil Corp.', 'XOM', 105.50, 80),
    ('Chevron Corp.', 'CVX', 160.80, 60),
    ('Ford Motor Co.', 'F', 14.25, 200),
    ('General Motors Co.', 'GM', 42.50, 150),
    ('Boeing Co.', 'BA', 230.75, 35),
    ('Uber Technologies', 'UBER', 55.60, 120),
    ('Airbnb Inc.', 'ABNB', 145.90, 50),
    ('Salesforce Inc.', 'CRM', 250.35, 30),
    ('Spotify Technology', 'SPOT', 160.25, 40),
    ('Snap Inc.', 'SNAP', 12.85, 300),
    ('Robinhood Markets', 'HOOD', 11.20, 500);