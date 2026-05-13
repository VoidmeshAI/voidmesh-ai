# ==========================================
# FILE: engines/entry_engine.py
# ==========================================


def generate_trade_levels(df, signal):

    try:

        # ==========================================
        # CURRENT PRICE
        # ==========================================

        current_price = float(df["close"].iloc[-1])

        # ==========================================
        # ATR STYLE RANGE
        # ==========================================

        recent_high = float(df["high"].tail(14).max())

        recent_low = float(df["low"].tail(14).min())

        range_size = recent_high - recent_low

        # SAFETY
        if range_size <= 0:

            range_size = current_price * 0.01

        # ==========================================
        # BUY SETUP
        # ==========================================

        if signal == "BUY":

            entry = round(current_price, 4)

            sl = round(current_price - (range_size * 0.5), 4)

            tp = round(current_price + (range_size * 1.5), 4)

        # ==========================================
        # SELL SETUP
        # ==========================================

        elif signal == "SELL":

            entry = round(current_price, 4)

            sl = round(current_price + (range_size * 0.5), 4)

            tp = round(current_price - (range_size * 1.5), 4)

        else:

            return None

        # ==========================================
        # RISK REWARD
        # ==========================================

        risk = abs(entry - sl)

        reward = abs(tp - entry)

        if risk == 0:

            rr = 0

        else:

            rr = round(reward / risk, 2)

        # ==========================================
        # RETURN
        # ==========================================

        return {"entry": entry, "sl": sl, "tp": tp, "rr": rr}

    except Exception as e:

        print(f"[red]ENTRY ENGINE ERROR:[/red] {e}")

        return None
