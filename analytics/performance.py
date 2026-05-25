import sqlite3
import pandas as pd

DB_NAME = "trading_agent.db"

# =========================================
# Load Trades
# =========================================

def load_trades():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM trades
    ORDER BY id ASC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

# =========================================
# Performance Metrics
# =========================================

def calculate_metrics():

    df = load_trades()

    if df.empty:

        return {
            "total_profit": 0,
            "win_rate": 0,
            "total_trades": 0,
            "wins": 0,
            "losses": 0
        }

    profits = []

    open_positions = {}

    wins = 0
    losses = 0

    for _, row in df.iterrows():

        symbol = row["symbol"]
        trade_type = row["type"]
        price = row["price"]
        qty = row["quantity"]

        if trade_type == "BUY":

            open_positions[symbol] = {
                "price": price,
                "qty": qty
            }

        elif trade_type == "SELL":

            if symbol in open_positions:

                buy_price = open_positions[symbol]["price"]

                pnl = (price - buy_price) * qty

                profits.append(pnl)

                if pnl > 0:
                    wins += 1
                else:
                    losses += 1

                del open_positions[symbol]

    total_profit = round(sum(profits), 2)

    total_trades = wins + losses

    if total_trades > 0:
        win_rate = round((wins / total_trades) * 100, 2)
    else:
        win_rate = 0

    return {

        "total_profit": total_profit,
        "win_rate": win_rate,
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "profits": profits
    }

# =========================================
# Equity Curve
# =========================================

def equity_curve():

    metrics = calculate_metrics()

    profits = metrics["profits"]

    equity = [10000]

    current = 10000

    for pnl in profits:

        current += pnl

        equity.append(round(current, 2))

    return equity