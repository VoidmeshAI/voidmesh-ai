# ==========================================
# FILE: data/websocket_client.py
# ==========================================

import json
import websocket

from rich import print

from core.realtime_scanner import run_realtime_scan

# ==========================================
# ON MESSAGE
# ==========================================


def on_message(ws, message):

    try:

        data = json.loads(message)

        payload = data["data"]

        candle = payload["k"]

        symbol = candle["s"]

        is_closed = candle["x"]

        close_price = candle["c"]

        # ONLY CLOSED CANDLES
        if is_closed:

            print(f"\n[bold green]" f"{symbol} CLOSED" f"[/bold green]")

            print(f"CLOSE PRICE: " f"{close_price}")

            # RUN AI
            run_realtime_scan(symbol)

    except Exception as e:

        print(f"\n[bold red]" f"MESSAGE ERROR:" f"[/bold red] " f"{e}")


# ==========================================
# ON ERROR
# ==========================================


def on_error(ws, error):

    print(f"\n[bold red]" f"WEBSOCKET ERROR:" f"[/bold red] " f"{error}")


# ==========================================
# ON CLOSE
# ==========================================


def on_close(ws, close_status_code, close_msg):

    print("\n[bold yellow]" "WEBSOCKET CLOSED" "[/bold yellow]")


# ==========================================
# ON OPEN
# ==========================================


def on_open(ws):

    print("\n[bold cyan]" "MULTI-SYMBOL WEBSOCKET CONNECTED" "[/bold cyan]")


# ==========================================
# START WEBSOCKET
# ==========================================


def start_websocket():

    streams = [
        "btcusdt@kline_15m",
        "ethusdt@kline_15m",
        "solusdt@kline_15m",
        "xrpusdt@kline_15m",
        "dogeusdt@kline_15m",
    ]

    stream_url = "/".join(streams)

    socket = "wss://stream.binance.com:9443/stream?streams=" f"{stream_url}"

    ws = websocket.WebSocketApp(
        socket,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(ping_interval=20, ping_timeout=10)
