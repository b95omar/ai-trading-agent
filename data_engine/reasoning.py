from openai import OpenAI

# =========================================
# OpenAI Client
# =========================================

# Replace with your API key
API_KEY = "YOUR_OPENAI_API_KEY"

client = OpenAI(api_key=API_KEY)

# =========================================
# AI Trade Reasoning
# =========================================

def generate_trade_reason(stock):

    prompt = f"""
    You are an advanced AI trading analyst.

    Analyze this stock data and explain whether
    this is a good trade opportunity.

    Stock Data:
    Symbol: {stock['symbol']}
    Price: {stock['price']}
    RSI: {stock['rsi']}
    MACD: {stock['macd']}
    AI Score: {stock['ai_score']}
    Signal: {stock['signal']}

    Give:
    1. Short market analysis
    2. Risk level
    3. Trade opinion
    4. Final recommendation

    Keep response under 120 words.
    """

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )

    return response.choices[0].message.content