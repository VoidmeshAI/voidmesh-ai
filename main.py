# ==========================================
# FILE: main.py
# ==========================================

import time
import logging
import database.models

from datetime import datetime

from rich import print

from telegram.send_message import send_telegram_message

from data.market_data import get_dataframe

from engines.trend_engine import get_trend
from engines.btc_filter import btc_market_filter
from engines.volatility_engine import get_volatility
from engines.regime_engine import detect_regime
from engines.probability_engine import calculate_confidence
from engines.no_trade_engine import should_trade
from engines.signal_engine import generate_signal
from engines.entry_engine import generate_trade_levels

from core.tracker import save_trade
from core.signal_memory import last_signals
from ai.predictor import predict_trade_probability
from engines.orderflow_engine import analyze_orderflow
from engines.liquidity_engine import detect_liquidity_sweep
from ai.features import extract_features

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    filename="logs/live_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s"
)


# ==========================================
# CONFIG
# ==========================================

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]

SCAN_INTERVAL = 60


# ==========================================
# SCAN SYMBOL
# ==========================================


def scan_symbol(symbol):

    try:

        # ==========================================
        # FETCH DATA
        # ==========================================

        df = get_dataframe(symbol)

        if df is None or len(df) == 0:

            print(f"[red]NO DATA FOR {symbol}[/red]")

            return

        candle_time = datetime.fromtimestamp(df["time"].iloc[-1] / 1000)

        # ==========================================
        # ENGINES
        # ==========================================

        trend = get_trend(df)

        volatility = get_volatility(df)

        orderflow = analyze_orderflow(df)

        liquidity = detect_liquidity_sweep(df)

        btc_state = btc_market_filter(trend, volatility)

        regime = detect_regime(df)

        confidence, reasons = calculate_confidence(trend, btc_state, volatility, regime)

        # ==========================================
        # CONFIDENCE SAFETY
        # ==========================================

        confidence = max(0, min(confidence, 100))

        # ==========================================
        # NO TRADE FILTER
        # ==========================================

        trade_allowed, no_trade_reasons = should_trade(confidence, regime, volatility)

        # ==========================================
        # SIGNAL ENGINE
        # ==========================================

        signal = generate_signal(trend, btc_state, confidence, trade_allowed)

        if signal not in ["BUY", "SELL"]:

            print(f"\n[bold yellow]{symbol}[/bold yellow]")

            print("[bold red]NO TRADE SIGNAL[/bold red]")

            return

        # ==========================================
        # TRADE LEVELS
        # ==========================================

        trade_setup = generate_trade_levels(df, signal)

        if not trade_setup:

            print(f"[bold red]" f"NO TRADE SETUP FOR {symbol}" f"[/bold red]")

            return

        # ==========================================
        # PREPARE AI FEATURES
        # ==========================================

        features = {}

        features["confidence"] = confidence

        # TREND
        if trend == "BULLISH":

            features["trend"] = 1

        else:

            features["trend"] = -1

        # BTC STATE
        if btc_state == "STRONG_BULLISH":

            features["btc_state"] = 1

        elif btc_state == "STRONG_BEARISH":

            features["btc_state"] = -1

        else:

            features["btc_state"] = 0

        # REGIME
        if regime == "TRENDING":

            features["regime"] = 1

        else:

            features["regime"] = 0

        # RR
        features["rr"] = float(trade_setup["rr"])

        # EXTRA FEATURES
        real_features = extract_features(df)

        features.update(real_features)

        # ==========================================
        # AI PROBABILITY
        # ==========================================

        ai_probability = predict_trade_probability(features)

        if ai_probability < 60:

            print("[red]AI FILTER BLOCKED TRADE[/red]")

            return

        # ==========================================
        # SIGNAL MEMORY
        # ==========================================

        current_signal = signal

        previous_signal = last_signals.get(symbol)

        signal_id = f"{symbol}_{int(time.time())}"

        # ==========================================
        # TELEGRAM ALERT
        # ==========================================

        if current_signal in ["BUY", "SELL"] and current_signal != previous_signal:

            formatted_reasons = "\n• ".join(reasons)

            message = f"""
🚨 VOIDMESH AI SIGNAL

🆔 SIGNAL ID:
{signal_id}

📊 PAIR:
{symbol}

📈 SIGNAL:
{signal}

🧠 CONFIDENCE:
{confidence}%

🤖 AI MODEL:
{ai_probability}%

🌍 MARKET:
{btc_state}

⚡ VOLATILITY:
{volatility}

📌 REGIME:
{regime}

💰 ENTRY:
{trade_setup['entry']}

🛑 STOP LOSS:
{trade_setup['sl']}

🎯 TAKE PROFIT:
{trade_setup['tp']}

⚖️ R:R:
{trade_setup['rr']}

🕒 CANDLE TIME:
{candle_time}

🤖 AI REASONS:
• {formatted_reasons}
"""

            # SEND TELEGRAM MESSAGE
            send_telegram_message(message)

            # SAVE LAST SIGNAL
            last_signals[symbol] = current_signal

            # LOG SIGNAL
            logging.info(
                f"{symbol} | " f"{signal} | " f"{confidence}% | " f"{btc_state}"
            )

            # SAVE TRADE
            save_trade(
                {
                    "signal_id": signal_id,
                    "symbol": symbol,
                    "signal": signal,
                    "confidence": confidence,
                    "trend": trend,
                    "btc_state": btc_state,
                    "volatility": volatility,
                    "regime": regime,
                    "entry": trade_setup["entry"],
                    "sl": trade_setup["sl"],
                    "tp": trade_setup["tp"],
                    "rr": trade_setup["rr"],
                    "time": str(datetime.now()),
                }
            )

        # ==========================================
        # TERMINAL OUTPUT
        # ==========================================

        print("\n========================")

        print(f"\n[bold cyan]{symbol}[/bold cyan]")

        print(f"[bold green]TREND:[/bold green] " f"{trend}")

        print(f"[bold yellow]BTC MARKET:[/bold yellow] " f"{btc_state}")

        print(f"[bold magenta]VOLATILITY:[/bold magenta] " f"{volatility}")

        print(f"[bold yellow]" f"ORDERFLOW:" f"[/bold yellow] " f"{orderflow['bias']}")

        print(
            f"[bold cyan]"
            f"ORDERFLOW STRENGTH:"
            f"[/bold cyan] "
            f"{orderflow['strength']}%"
        )

        print(
            f"[bold magenta]" f"LIQUIDITY:" f"[/bold magenta] " f"{liquidity['signal']}"
        )

        print(f"[bold blue]REGIME:[/bold blue] " f"{regime}")

        print(f"[bold red]AI CONFIDENCE:[/bold red] " f"{confidence}%")

        print(
            f"[bold magenta]"
            f"AI MODEL PROBABILITY:"
            f"[/bold magenta] "
            f"{ai_probability}%"
        )

        # ==========================================
        # FINAL HYBRID AI SCORE
        # ==========================================

        final_ai_score = round((confidence * 0.85) + (ai_probability * 0.15), 2)

        # ==========================================
        # FINAL AI FILTER
        # ==========================================

        if final_ai_score < 50:

            print("[bold red]" "LOW AI SCORE SKIPPED" "[/bold red]")

            return

        print(f"[bold green]" f"FINAL AI SCORE:" f"[/bold green] " f"{final_ai_score}%")

        print("\n[bold white]AI REASONS:[/bold white]")

        for r in reasons:

            print(f"• {r}")

        print(f"\n[bold cyan]SIGNAL:[/bold cyan] " f"{signal}")

        if trade_setup:

            print("\n[bold green]TRADE SETUP:[/bold green]")

            print(f"ENTRY: " f"{trade_setup['entry']}")

            print(f"STOP LOSS: " f"{trade_setup['sl']}")

            print(f"TAKE PROFIT: " f"{trade_setup['tp']}")

            print(f"R:R: " f"{trade_setup['rr']}")

        print("\n[bold white]TRADE DECISION:[/bold white]")

        if trade_allowed:

            print("[bold green]TRADE ALLOWED[/bold green]")

        else:

            print("[bold red]NO TRADE[/bold red]")

            print("\n[bold yellow]REASONS:[/bold yellow]")

            for r in no_trade_reasons:

                print(f"• {r}")

    except Exception as e:

        logging.error(f"{symbol} ERROR: {e}")

        print(f"\n[bold red]ERROR SCANNING " f"{symbol}[/bold red]")

        print(e)


# ==========================================
# START BOT
# ==========================================

print("\n[bold green]VOIDMESH AI STARTED[/bold green]")


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    try:

        print(f"\n[bold white]SCAN TIME:[/bold white] " f"{datetime.now()}")

        for symbol in symbols:

            scan_symbol(symbol)

            # RATE LIMIT SAFETY
            time.sleep(1)

        # WAIT NEXT SCAN
        time.sleep(SCAN_INTERVAL)

    except Exception as e:

        logging.error(f"MAIN LOOP ERROR: {e}")

        print("\n[bold red]MAIN LOOP ERROR[/bold red]")

        print(e)

        time.sleep(5)
