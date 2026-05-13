import requests

BOT_TOKEN = "8694829636:AAHZWUqPcLuX5dohjrD0sSSdtpvJS6zCpg4"

CHAT_ID = "8019403377"


def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)