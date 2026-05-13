# ==========================================
# FILE: execution/binance_executor.py
# ==========================================

from rich import print


def place_order(symbol, side, quantity=0):

    print(f"\n[bold yellow]" f"BINANCE DISABLED:" f"[/bold yellow] " f"{symbol} {side}")

    return {"status": "DISABLED"}
