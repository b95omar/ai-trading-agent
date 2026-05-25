import math

# =========================================
# Risk & Strategy Engine
# =========================================

class StrategyEngine:

    def __init__(self):

        self.max_risk_per_trade = 0.02   # 2% risk per trade
        self.max_exposure = 0.50         # max 50% capital in market

    # =========================================
    # Calculate Position Size
    # =========================================

    def position_size(self, balance, confidence_score):

        # Higher confidence → bigger position
        risk_factor = confidence_score / 100

        risk_amount = balance * self.max_risk_per_trade * risk_factor

        return max(10, round(risk_amount, 2))

    # =========================================
    # Risk Score (0–100)
    # =========================================

    def risk_score(self, stock):

        score = 50

        # RSI filters
        if stock["rsi"] > 70:
            score += 20  # overbought risk
        elif stock["rsi"] < 30:
            score -= 10  # potential opportunity

        # MACD momentum
        if stock["macd"] > 0:
            score -= 10
        else:
            score += 10

        # AI score impact
        score -= (stock["ai_score"] - 50) * 0.3

        return max(0, min(100, score))

    # =========================================
    # Final Trade Decision
    # =========================================

    def should_trade(self, stock):

        risk = self.risk_score(stock)

        if risk > 70:
            return "NO_TRADE"

        if stock["signal"] in ["STRONG BUY", "BUY"]:
            return "BUY"

        if stock["signal"] == "SELL":
            return "SELL"

        return "HOLD"