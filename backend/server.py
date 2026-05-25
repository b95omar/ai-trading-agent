import sys
import os

# =========================================
# Fix Imports
# =========================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# =========================================
# Imports
# =========================================
from market.live_data import get_chart_data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ml.predictor import train_model
from data_engine.scanner import get_top_stocks
from execution_engine.paper_trader import PaperTrader
from database.database import get_recent_trades
from ai_engine.reasoning import generate_trade_reason

from analytics.performance import (
    calculate_metrics,
    equity_curve
)

# =========================================
# FastAPI
# =========================================

app = FastAPI(
    title="AI Trading Agent",
    version="5.0"
)

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# Trader
# =========================================

trader = PaperTrader(10000)

# =========================================
# Home
# =========================================

@app.get("/")
def home():

    return {
        "status": "AI Trading Agent Running"
    }

# =========================================
# Stocks
# =========================================

@app.get("/top-stocks")
def top_stocks():

    return {
        "data": get_top_stocks()
    }

# =========================================
# Portfolio
# =========================================

@app.get("/portfolio")
def portfolio():

    return trader.portfolio()

# =========================================
# Trades
# =========================================

@app.get("/trades")
def trades():

    return {
        "recent_trades": get_recent_trades()
    }

# =========================================
# AI Reasoning
# =========================================

@app.get("/reason/{symbol}")
def reason(symbol: str):

    stocks = get_top_stocks()

    stock_data = None

    for stock in stocks:

        if stock["symbol"] == symbol:
            stock_data = stock
            break

    if stock_data is None:

        return {
            "error": "Stock not found"
        }

    analysis = generate_trade_reason(stock_data)

    return {
        "symbol": symbol,
        "analysis": analysis
    }

# =========================================
# Performance Metrics
# =========================================

@app.get("/performance")
def performance():

    return calculate_metrics()

# =========================================
# Equity Curve
# =========================================

@app.get("/equity-curve")
def equity():

    return {
        "equity": equity_curve()
    }
# =========================================
# Live Candlestick Data
# =========================================

@app.get("/chart/{symbol}")
def chart(symbol: str):

    data = get_chart_data(symbol)

    return {
        "symbol": symbol,
        "candles": data
    }
# =========================================
# Buy
# =========================================

@app.post("/buy")
def buy(symbol: str, price: float, amount: float):

    return trader.buy(
        symbol=symbol,
        price=price,
        amount_usd=amount
    )

# =========================================
# Sell
# =========================================

@app.post("/sell")
def sell(symbol: str, price: float, quantity: float = None):

    return trader.sell(
        symbol=symbol,
        price=price,
        quantity=quantity
    )
# =========================================
# ML Prediction
# =========================================

@app.get("/predict/{symbol}")
def predict(symbol: str):

    result = train_model(symbol)

    return result