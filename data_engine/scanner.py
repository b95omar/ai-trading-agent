import yfinance as yf
import pandas as pd

from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

# =========================================
# AI Trading Agent - SMART Scanner v2
# =========================================

def get_top_stocks():

    stocks = [
        "AAPL", "TSLA", "NVDA", "MSFT", "AMD",
        "META", "AMZN", "PLTR", "GOOGL", "NFLX",
        "INTC", "UBER"
    ]

    MIN_PRICE = 5
    MAX_PRICE = 500

    results = []

    for symbol in stocks:

        try:
            ticker = yf.Ticker(symbol)

            # Get 3 months of data for analysis
            hist = ticker.history(period="3mo")

            if hist.empty:
                continue

            price = hist["Close"].iloc[-1]

            # Price filter
            if not (MIN_PRICE <= price <= MAX_PRICE):
                continue

            # =========================================
            # TECHNICAL INDICATORS
            # =========================================

            rsi = RSIIndicator(hist["Close"], window=14).rsi().iloc[-1]
            macd = MACD(hist["Close"]).macd_diff().iloc[-1]
            ema20 = EMAIndicator(hist["Close"], window=20).ema_indicator().iloc[-1]
            ema50 = EMAIndicator(hist["Close"], window=50).ema_indicator().iloc[-1]

            # =========================================
            # AI SCORING ENGINE (REAL LOGIC)
            # =========================================

            score = 50  # base score

            # RSI logic
            if rsi < 30:
                score += 25  # oversold = bullish bounce

            elif rsi < 45:
                score += 10

            elif rsi > 70:
                score -= 25  # overbought = risk

            # MACD momentum
            if macd > 0:
                score += 20
            else:
                score -= 10

            # Trend (EMA crossover logic)
            if ema20 > ema50:
                score += 20  # uptrend confirmed
            else:
                score -= 15  # downtrend

            # Price vs EMA
            if price > ema20:
                score += 10
            else:
                score -= 10

            # Clamp score
            score = max(1, min(100, score))

            # =========================================
            # SIGNAL GENERATION
            # =========================================

            if score >= 80:
                signal = "STRONG BUY"
            elif score >= 60:
                signal = "BUY"
            elif score >= 40:
                signal = "HOLD"
            else:
                signal = "SELL"

            # =========================================
            # ADD RESULT
            # =========================================

            results.append({
                "symbol": symbol,
                "price": round(price, 2),
                "rsi": round(rsi, 2),
                "macd": round(macd, 4),
                "ema20": round(ema20, 2),
                "ema50": round(ema50, 2),
                "ai_score": score,
                "signal": signal
            })

        except Exception as e:
            print(f"Error with {symbol}: {e}")

    # =========================================
    # SORT + TOP 10
    # =========================================

    df = pd.DataFrame(results)
    df = df.sort_values(by="ai_score", ascending=False)

    return df.head(10).to_dict(orient="records")


# =========================================
# TEST MODE
# =========================================

if __name__ == "__main__":

    data = get_top_stocks()

    print("\nTOP 10 AI PICKS\n")
    for d in data:
        print(d)