def calculate_metrics(results):

    total = len(results)

    wins = 0

    losses = 0

    pnl = 0

    for r in results:

        if r["result"] == "WIN":

            wins += 1

            pnl += r["rr_result"]

        elif r["result"] == "LOSS":

            losses += 1

            pnl += r["rr_result"]

    winrate = 0

    if total > 0:

        winrate = round((wins / total) * 100, 2)

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "winrate": winrate,
        "total_rr": round(pnl, 2),
    }
