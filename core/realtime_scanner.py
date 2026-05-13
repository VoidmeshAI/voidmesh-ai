# ==========================================
# FILE: core/realtime_scanner.py
# ==========================================

from rich import print

from data.market_data import get_dataframe
from datetime import datetime
from engines.trend_engine import get_trend
from engines.btc_filter import btc_market_filter
from engines.volatility_engine import get_volatility
from engines.regime_engine import detect_regime
from engines.signal_engine import generate_signal
from engines.entry_engine import generate_trade_levels

from engines.orderflow_engine import analyze_orderflow
from engines.liquidity_engine import detect_liquidity_sweep

from ai.features import extract_features
from ai.predictor import predict_trade_probability

from telegram.send_message import send_telegram_message

from core.signal_memory import last_signals
from papertrade.tracker import open_trade, check_trades
from papertrade.stats import show_stats
from papertrade.pnl import show_pnl
from core.signal_history import signal_history
from database.db import cursor, conn
from execution.binance_executor import place_order
from papertrade.portfolio import portfolio
from risk.position_sizing import calculate_position_size
from risk.leverage_engine import calculate_leverage
from risk.exposure_engine import check_portfolio_exposure
from ai.retrain import retrain_ai
from ai.retrain_state import last_retrain_count
from ai import retrain_state
from agents.battle_manager import run_agent_battle
from copytrading.copier import copy_trade

# ==========================================
# REALTIME SCANNER
# ==========================================


def run_realtime_scan(symbol):

    try:

        print(f"\n[bold cyan]" f"SCANNING {symbol}" f"[/bold cyan]")

        # ==========================================
        # FETCH DATA
        # ==========================================

        df = get_dataframe(symbol=symbol, interval="15m", limit=200)

        battle_results = run_agent_battle(df)

        if df is None or len(df) == 0:

            print("[bold red]" "NO DATA" "[/bold red]")

            return
        current_price = df["close"].iloc[-1]

        check_trades(symbol, current_price)

        # ==========================================
        # ENGINES
        # ==========================================

        trend = get_trend(df)

        volatility = get_volatility(df)

        btc_state = btc_market_filter(trend, volatility)

        regime = detect_regime(df)

        orderflow = analyze_orderflow(df)

        liquidity = detect_liquidity_sweep(df)

        # ==========================================
        # FEATURES
        # ==========================================

        features = extract_features(df)

        # ==========================================
        # BASE CONFIDENCE
        # ==========================================

        confidence = 70

        # ==========================================
        # SIGNAL
        # ==========================================

        signal = generate_signal(trend, btc_state, confidence, True)

        if signal not in ["BUY", "SELL"]:

            print("[bold yellow]" "NO SIGNAL" "[/bold yellow]")

            return

        # ==========================================
        # PORTFOLIO EXPOSURE
        # ==========================================

        exposure = check_portfolio_exposure()

        if not exposure["allowed"]:

            print(
                f"[bold red]"
                f"EXPOSURE BLOCKED:"
                f"[/bold red] "
                f"{exposure['reason']}"
            )

            return

        # ==========================================
        # TRADE LEVELS
        # ==========================================

        trade_setup = generate_trade_levels(df, signal)

        if not trade_setup:

            print("[bold red]" "NO TRADE SETUP" "[/bold red]")

            return

        # ==========================================
        # DUPLICATE SIGNAL PROTECTION
        # ==========================================

        previous_signal = last_signals.get(symbol)

        if previous_signal == signal:

            print("[bold yellow]" "DUPLICATE SIGNAL SKIPPED" "[/bold yellow]")

            return

        # ==========================================
        # PREPARE AI FEATURES
        # ==========================================

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

        # ==========================================
        # AI PROBABILITY
        # ==========================================

        try:

            ai_probability = predict_trade_probability(features)

        except Exception as e:

            print(f"[red]AI ERROR:[/red] {e}")

            ai_probability = 50

        # ==========================================
        # LEVERAGE
        # ==========================================

        leverage = calculate_leverage(ai_probability, volatility, regime)

        # ==========================================
        # POSITION SIZE
        # ==========================================

        position_size = calculate_position_size(
            balance=portfolio["current_balance"],
            risk_percent=1,
            entry=trade_setup["entry"],
            sl=trade_setup["sl"],
            leverage=leverage,
        )

        # ==========================================
        # TELEGRAM MESSAGE
        # ==========================================

        message = f"""
🚨 VOIDMESH AI SIGNAL

📊 PAIR:
{symbol}

📈 SIGNAL:
{signal}

🧠 AI PROBABILITY:
{round(ai_probability, 2)}%

🌍 REGIME:
{regime}

⚡ VOLATILITY:
{volatility}

🌊 ORDERFLOW:
{orderflow['bias']}

💧 LIQUIDITY:
{liquidity['signal']}

💰 ENTRY:
{trade_setup['entry']}

🛑 STOP LOSS:
{trade_setup['sl']}

🎯 TAKE PROFIT:
{trade_setup['tp']}

⚖️ R:R:
{trade_setup['rr']}

💰 POSITION SIZE:
{position_size}

⚡ LEVERAGE:
{leverage}x
"""

        # ==========================================
        # SEND TELEGRAM ALERT
        # ==========================================

        send_telegram_message(message)

        last_signals[symbol] = signal

        # place_order(symbol, signal, position_size)

        copy_trade("VOIDMESH_AI", symbol, signal, trade_setup["entry"])

        open_trade(
            symbol, signal, trade_setup["entry"], trade_setup["sl"], trade_setup["tp"]
        )

        show_stats()

        show_pnl()

        # ==========================================
        # AUTO RETRAIN
        # ==========================================

        total_trades = len(signal_history)

        if (
            total_trades > 0
            and total_trades % 20 == 0
            and retrain_state.last_retrain_count != total_trades
        ):

            retrain_ai()

        retrain_state.last_retrain_count = total_trades

        # ==========================================
        # SAVE LAST SIGNAL
        # ==========================================

        signal_history.append(
            {
                "symbol": symbol,
                "signal": signal,
                "probability": ai_probability,
                "regime": regime,
                "orderflow": orderflow["bias"],
                "liquidity": liquidity["signal"],
                "time": str(datetime.now()),
            }
        )

        cursor.execute(
            """
            INSERT INTO signals (

                symbol,
                signal,
                probability,
                regime,
                orderflow,
                liquidity

            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                signal,
                ai_probability,
                regime,
                orderflow["bias"],
                liquidity["signal"],
            ),
        )

        conn.commit()

        # ==========================================
        # OUTPUT
        # ==========================================

        print(f"\nTREND: {trend}")

        print(f"VOLATILITY: {volatility}")

        print(f"REGIME: {regime}")

        print(f"ORDERFLOW: " f"{orderflow['bias']}")

        print(f"LIQUIDITY: " f"{liquidity['signal']}")

        print(f"\nSIGNAL: {signal}")

        print(f"AI PROBABILITY: " f"{ai_probability}%")

        print(f"\nENTRY: " f"{trade_setup['entry']}")

        print(f"SL: " f"{trade_setup['sl']}")

        print(f"TP: " f"{trade_setup['tp']}")

        print(f"POSITION SIZE: " f"{position_size}")

        print(f"LEVERAGE: " f"{leverage}x")

    except Exception as e:

        print(f"\n[bold red]" f"ERROR SCANNING {symbol}" f"[/bold red]")

        print(e)
