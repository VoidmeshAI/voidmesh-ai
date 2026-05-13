def simulate_trade(future_df, signal, trade_setup):

    sl = trade_setup["sl"]

    tp = trade_setup["tp"]

    rr = trade_setup["rr"]

    for _, row in future_df.iterrows():

        high = row["high"]

        low = row["low"]

        # BUY
        if signal == "BUY":

            if low <= sl:

                return {"result": "LOSS", "rr": -1}

            if high >= tp:

                return {"result": "WIN", "rr": rr}

        # SELL
        elif signal == "SELL":

            if high >= sl:

                return {"result": "LOSS", "rr": -1}

            if low <= tp:

                return {"result": "WIN", "rr": rr}

    return {"result": "OPEN", "rr": 0}
