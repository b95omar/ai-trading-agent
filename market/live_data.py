import yfinance as yf

# =========================================
# Get Candlestick Data
# =========================================

def get_chart_data(symbol="NVDA", period="1d", interval="5m"):

    try:

        ticker = yf.Ticker(symbol)

        df = ticker.history(
            period=period,
            interval=interval
        )

        candles = []

        for index, row in df.iterrows():

            candles.append({

                "time": index.strftime("%H:%M"),

                "open": round(row["Open"], 2),

                "high": round(row["High"], 2),

                "low": round(row["Low"], 2),

                "close": round(row["Close"], 2)
            })

        return candles

    except Exception as e:

        return {
            "error": str(e)
        }