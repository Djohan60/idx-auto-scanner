
import yfinance as yf
import pandas as pd

STOCK_LIST = [
    "BBCA.JK","BBRI.JK","BMRI.JK","TLKM.JK","ASII.JK",
    "MDKA.JK","ANTM.JK","ICBP.JK","INDF.JK"
]

def to_float(v):
    try:
        return float(v)
    except:
        return None

def scan_market():

    results = []
    ranking = []

    for stock in STOCK_LIST:
        try:
            data = yf.download(stock, period="3mo", progress=False)

            if data is None or len(data) < 60:
                continue

            close = data["Close"]

            ma20 = close.rolling(20).mean().iloc[-1]
            ma50 = close.rolling(50).mean().iloc[-1]
            last = close.iloc[-1]

            ma20 = to_float(ma20)
            ma50 = to_float(ma50)
            last = to_float(last)

            if not ma20 or not ma50 or not last:
                continue

            score = float((last/ma20) + (ma20/ma50))

            ranking.append((score, stock, last, ma20, ma50))

            # Uptrend kuat
            if last > ma20 and ma20 > ma50:

                entry = round(last,0)
                sl = round(ma20 * 0.97,0)
                tp = round(entry + (entry - sl) * 2,0)

                results.append({
                    "stock": stock,
                    "price": entry,
                    "sl": sl,
                    "tp": tp
                })

        except Exception as e:
            continue

    # Jika kosong → ambil kandidat terbaik
    if len(results) == 0 and len(ranking) > 0:

        ranking = sorted(ranking, key=lambda x: x[0], reverse=True)
        best = ranking[:3]

        for s in best:
            entry = round(s[2],0)
            sl = round(s[3] * 0.97,0)
            tp = round(entry + (entry - sl) * 1.5,0)

            results.append({
                "stock": s[1] + " (Early Trend)",
                "price": entry,
                "sl": sl,
                "tp": tp
            })

    return results
