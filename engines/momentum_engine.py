from ta.momentum import RSIIndicator


def get_momentum(df):

    rsi = RSIIndicator(close=df["close"], window=14).rsi()

    last_rsi = rsi.iloc[-1]

    if last_rsi > 60:

        return "BULLISH"

    elif last_rsi < 40:

        return "BEARISH"

    return "NEUTRAL"
