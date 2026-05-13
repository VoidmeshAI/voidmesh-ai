# ==========================================
# FILE: execution/binance_executor.py
# ==========================================

import os

from dotenv import load_dotenv

from binance.client import Client

from rich import print

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")

API_SECRET = os.getenv("BINANCE_API_SECRET")

# ==========================================
# CLIENT
# ==========================================

client = Client(API_KEY, API_SECRET)

client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"


# ==========================================
# EXECUTE ORDER
# ==========================================


def place_order(symbol, side, quantity):

    try:

        order_side = "BUY" if side == "BUY" else "SELL"

        order = client.futures_create_order(
            symbol=symbol, side=order_side, type="MARKET", quantity=quantity
        )

        print(f"\n[bold green]" f"ORDER EXECUTED:" f"[/bold green] " f"{symbol} {side}")

        return order

    except Exception as e:

        print(f"\n[bold red]" f"ORDER ERROR:" f"[/bold red] " f"{e}")

        return None
