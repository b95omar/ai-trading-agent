from datetime import datetime

from database.database import (
    init_db,
    save_trade,
    save_portfolio
)

# =========================================
# Initialize Database
# =========================================

init_db()

# =========================================
# Paper Trading Engine
# =========================================

class PaperTrader:

    def __init__(self, initial_balance=10000):

        self.balance = initial_balance

        self.positions = {}

        self.trade_history = []

    # =========================================
    # BUY
    # =========================================

    def buy(self, symbol, price, amount_usd):

        if amount_usd > self.balance:

            return {
                "error": "Not enough balance"
            }

        quantity = amount_usd / price

        self.balance -= amount_usd

        if symbol in self.positions:
            self.positions[symbol] += quantity
        else:
            self.positions[symbol] = quantity

        trade = {
            "type": "BUY",
            "symbol": symbol,
            "price": price,
            "quantity": quantity,
            "time": str(datetime.now())
        }

        self.trade_history.append(trade)

        # Save to DB
        save_trade(trade)

        save_portfolio(self.balance)

        return {
            "message": "BUY executed",
            "symbol": symbol,
            "quantity": quantity,
            "balance": self.balance
        }

    # =========================================
    # SELL
    # =========================================

    def sell(self, symbol, price, quantity=None):

        if symbol not in self.positions:

            return {
                "error": "No position found"
            }

        owned_qty = self.positions[symbol]

        if quantity is None:
            quantity = owned_qty

        if quantity > owned_qty:
            quantity = owned_qty

        self.balance += quantity * price

        self.positions[symbol] -= quantity

        if self.positions[symbol] <= 0:
            del self.positions[symbol]

        trade = {
            "type": "SELL",
            "symbol": symbol,
            "price": price,
            "quantity": quantity,
            "time": str(datetime.now())
        }

        self.trade_history.append(trade)

        # Save to DB
        save_trade(trade)

        save_portfolio(self.balance)

        return {
            "message": "SELL executed",
            "symbol": symbol,
            "quantity": quantity,
            "balance": self.balance
        }

    # =========================================
    # Portfolio
    # =========================================

    def portfolio(self):

        return {
            "balance": self.balance,
            "positions": self.positions,
            "trade_count": len(self.trade_history),
            "recent_trades": self.trade_history[-10:]
        }