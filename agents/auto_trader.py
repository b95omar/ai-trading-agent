import sys
import os
import time

# =========================================
# Fix Imports
# =========================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# =========================================
# Imports
# =========================================

from data_engine.scanner import get_top_stocks

from execution_engine.paper_trader import PaperTrader

from strategy.engine import StrategyEngine

from notifications.telegram_bot import (
    send_telegram_message
)

# =========================================
# AI Trading Bot
# =========================================

class AutoTrader:

    def __init__(self):

        self.trader = PaperTrader(10000)

        self.strategy = StrategyEngine()

        self.last_actions = {}

    # =========================================
    # Run Cycle
    # =========================================

    def run_cycle(self):

        print("\n==========================")
        print("AI TRADING ENGINE")
        print("==========================\n")

        stocks = get_top_stocks()

        for stock in stocks:

            symbol = stock["symbol"]

            decision = self.strategy.should_trade(stock)

            risk = self.strategy.risk_score(stock)

            print(
                f"{symbol} | "
                f"Signal: {stock['signal']} | "
                f"Risk: {risk} | "
                f"Decision: {decision}"
            )

            # =========================================
            # BUY
            # =========================================

            if decision == "BUY":

                if self.last_actions.get(symbol) != "BUY":

                    size = self.strategy.position_size(
                        self.trader.balance,
                        stock["ai_score"]
                    )

                    result = self.trader.buy(
                        symbol=symbol,
                        price=stock["price"],
                        amount_usd=size
                    )

                    print("BUY:", result)

                    # Telegram Alert
                    send_telegram_message(

                        f"""
🚀 BUY EXECUTED

Symbol: {symbol}

Price: ${stock['price']}

AI Score: {stock['ai_score']}

Risk Score: {risk}

Amount: ${round(size,2)}
"""
                    )

                    self.last_actions[symbol] = "BUY"

            # =========================================
            # SELL
            # =========================================

            elif decision == "SELL":

                if symbol in self.trader.positions:

                    result = self.trader.sell(
                        symbol=symbol,
                        price=stock["price"]
                    )

                    print("SELL:", result)

                    send_telegram_message(

                        f"""
📉 SELL EXECUTED

Symbol: {symbol}

Price: ${stock['price']}

AI Score: {stock['ai_score']}

Risk Score: {risk}
"""
                    )

                    self.last_actions[symbol] = "SELL"

        # =========================================
        # Portfolio Update
        # =========================================

        portfolio = self.trader.portfolio()

        print("\nPORTFOLIO:")
        print(portfolio)

    # =========================================
    # Start Loop
    # =========================================

    def start(self, interval=60):

        while True:

            try:

                self.run_cycle()

            except Exception as e:

                print("ERROR:", e)

            time.sleep(interval)

# =========================================
# Start Bot
# =========================================

if __name__ == "__main__":

    bot = AutoTrader()

    bot.start()