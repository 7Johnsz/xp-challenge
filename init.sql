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
    CodAsset BIGINT REFERENCES asset(CodAsset) ON DELETE CASCADE,
    CodClient BIGINT REFERENCES client(CodClient) ON DELETE CASCADE,
    quantity BIGINT NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (CodAsset, CodClient)
);

CREATE TABLE IF NOT EXISTS transaction (
    CodTransaction BIGSERIAL PRIMARY KEY,
    CodClient BIGINT REFERENCES client(CodClient) ON DELETE CASCADE,
    CodAsset BIGINT REFERENCES asset(CodAsset) ON DELETE CASCADE,
    quantity BIGINT NOT NULL CHECK (quantity > 0),
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),  
    transaction_type VARCHAR(4) NOT NULL CHECK (transaction_type IN ('BUY', 'SELL')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
