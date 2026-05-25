import sqlite3

# =========================================
# Database Connection
# =========================================

DB_NAME = "trading_agent.db"

# =========================================
# Create Database Tables
# =========================================

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # =========================================
    # Trades Table
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        type TEXT,
        symbol TEXT,
        price REAL,
        quantity REAL,
        timestamp TEXT
    )
    """)

    # =========================================
    # Portfolio Snapshots
    # =========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        balance REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================================
# Save Trade
# =========================================

def save_trade(trade):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO trades (
        type,
        symbol,
        price,
        quantity,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?)
    """, (

        trade["type"],
        trade["symbol"],
        trade["price"],
        trade["quantity"],
        trade["time"]

    ))

    conn.commit()
    conn.close()

# =========================================
# Save Portfolio Snapshot
# =========================================

def save_portfolio(balance):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO portfolio_history (
        balance,
        timestamp
    )
    VALUES (?, datetime('now'))
    """, (balance,))

    conn.commit()
    conn.close()

# =========================================
# Load Recent Trades
# =========================================

def get_recent_trades(limit=20):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM trades
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows