# ==========================================
# FILE: engines/volatility_engine.py
# ==========================================


def get_volatility(df):

    recent_high = df["high"].tail(20).max()

    recent_low = df["low"].tail(20).min()

    current_price = df["close"].iloc[-1]

    move = recent_high - recent_low

    volatility_percent = (move / current_price) * 100

    if volatility_percent > 4:

        return "HIGH_VOLATILITY"

    elif volatility_percent > 2:

        return "MEDIUM_VOLATILITY"

    return "LOW_VOLATILITY"
