from scanner import scan_market
import requests
from datetime import datetime

BOT_TOKEN = "8315072461:AAHhPZKkCBGUbVN5WW5DNiAmeVWGBaisLWY"
CHAT_ID = "711341023"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def main():

    results = scan_market()

    message = "📊 IDX AUTO SCANNER\n"
    message += f"{datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"

    if not results:
        message += "Tidak ada saham uptrend hari ini"
    else:
        for r in results:
            message += (
                f"{r['stock']}\n"
                f"Buy : {r['price']}\n"
                f"SL  : {r['sl']}\n"
                f"TP  : {r['tp']}\n\n"
            )

    send_telegram(message)

if __name__ == "__main__":
    main()
