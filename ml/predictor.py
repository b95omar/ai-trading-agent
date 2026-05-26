import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

# =========================================
# Load Data
# =========================================

def load_data(symbol="NVDA"):

    df = yf.download(
        symbol,
        period="1y",
        interval="1d"
    )

    df.dropna(inplace=True)

    return df

# =========================================
# Feature Engineering
# =========================================

def create_features(df):

    df["Return"] = df["Close"].pct_change()

    df["MA5"] = df["Close"].rolling(5).mean()

    df["MA10"] = df["Close"].rolling(10).mean()

    df["Volatility"] = (
        df["Return"].rolling(5).std()
    )

    df["Target"] = df["Close"].shift(-1)

    df.dropna(inplace=True)

    features = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "MA5",
        "MA10",
        "Volatility"
    ]

    X = df[features]

    y = df["Target"]

    return X, y, df

# =========================================
# Train Model
# =========================================

def train_model(symbol="NVDA"):

    df = load_data(symbol)

    X, y, full_df = create_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    error = mean_absolute_error(
        y_test,
        predictions
    )

    latest_features = X.iloc[-1:]

    # FORCE REAL FLOAT VALUES

    current_price = float(
        full_df["Close"].dropna().to_numpy().flatten()[-1]
    )

    current_price = float(
        full_df["Close"].values[-1]
    )

    # TREND

    if next_price > current_price:
        trend = "BULLISH"
    else:
        trend = "BEARISH"

    confidence = round(
        max(0, 100 - error),
        2
    )

    return {

        "symbol": symbol,

        "current_price": round(
            current_price,
            2
        ),

        "predicted_price": round(
            next_price,
            2
        ),

        "trend": trend,

        "confidence": confidence,

        "mae_error": round(
            float(error),
            2
        )
    }