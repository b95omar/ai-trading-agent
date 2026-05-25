import requests

# =========================================
# Telegram Config
# =========================================

BOT_TOKEN = "8690690866:AAGvGXtw6oUnqLz0McRvWgd_9ojBJGMgX8o"

CHAT_ID = "2080282628"

# =========================================
# Send Message
# =========================================

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        response = requests.post(
            url,
            json=payload
        )

        return response.json()

    except Exception as e:

        print("Telegram Error:", e)