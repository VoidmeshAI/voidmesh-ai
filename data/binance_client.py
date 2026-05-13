from binance.client import Client

client = Client()


def get_klines(symbol="BTCUSDT", interval="15m", limit=200):

    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    return klines
