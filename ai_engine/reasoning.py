def generate_trade_reason(stock):

    return f"""
AI ANALYSIS (LOCAL MODE)

Symbol: {stock['symbol']}
Price: {stock['price']}
RSI: {stock['rsi']}
MACD: {stock['macd']}
Score: {stock['ai_score']}
Signal: {stock['signal']}

Analysis:
- Market conditions are based on technical indicators
- RSI + MACD used for momentum detection
- AI score reflects combined signal strength

Risk Level:
- Moderate based on volatility signals

Recommendation:
- Follow signal direction with proper risk management
"""