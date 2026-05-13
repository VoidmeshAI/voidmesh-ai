# ==========================================
# FILE: dashboard.py
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px

from data.market_data import get_dataframe
from datetime import datetime
from engines.trend_engine import get_trend
from engines.volatility_engine import get_volatility
from engines.regime_engine import detect_regime

from engines.orderflow_engine import analyze_orderflow
from engines.liquidity_engine import detect_liquidity_sweep
from streamlit_autorefresh import st_autorefresh
from papertrade.portfolio import portfolio
from papertrade.equity import equity_curve
from database.db import cursor
from dashboard_utils.heatmap_data import generate_heatmap
from ai.predictor import predict_trade_probability
from engines.signal_engine import generate_signal

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(page_title="VOIDMESH AI", layout="wide")

st.title("🚀 VOIDMESH AI DASHBOARD")
st.caption(f"Last Update: " f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Realtime AI Trading Intelligence System")

# ==========================================
# AI HEATMAP
# ==========================================

st.subheader("🌍 AI Market Heatmap")

heatmap = generate_heatmap()

heatmap_df = pd.DataFrame(heatmap)

st.dataframe(heatmap_df, use_container_width=True)

# ==========================================
# SYSTEM STATUS
# ==========================================

st.success(
    "🟢 SYSTEM ONLINE | 🧠 AI ACTIVE | ⚡ WEBSOCKET CONNECTED | 🤖 TESTNET READY"
)

# ==========================================
# AUTO REFRESH
# ==========================================

st_autorefresh(interval=15000, key="voidmesh_refresh")

# ==========================================
# PORTFOLIO
# ==========================================

st.subheader("💰 Portfolio")

p1, p2, p3 = st.columns(3)

p1.metric("Balance", f"${portfolio['current_balance']}")

p2.metric("PNL", f"${portfolio['realized_pnl']}")

growth = (
    (portfolio["current_balance"] - portfolio["starting_balance"])
    / portfolio["starting_balance"]
) * 100

p3.metric("Growth", f"{round(growth, 2)}%")

# ==========================================
# SYMBOL
# ==========================================

symbol = st.selectbox(
    "Select Pair", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]
)

# ==========================================
# FETCH DATA
# ==========================================

df = get_dataframe(symbol=symbol, interval="15m", limit=200)

if df is None or len(df) == 0:

    st.error("No market data found")

    st.stop()

current_price = df["close"].iloc[-1]

st.metric("CURRENT PRICE", f"${round(current_price, 4)}")

# ==========================================
# ENGINES
# ==========================================

trend = get_trend(df)

volatility = get_volatility(df)

regime = detect_regime(df)

orderflow = analyze_orderflow(df)

liquidity = detect_liquidity_sweep(df)

# ==========================================
# CURRENT SIGNAL
# ==========================================

features = {
    "confidence": 70,
    "trend": trend,
    "btc_state": "STRONG_BULLISH",
    "regime": regime,
    "rr": 3,
    "rsi": 55,
    "macd": 1,
    "macd_signal": 1,
    "atr": 1,
    "ema_distance": 1,
    "volume_spike": 1,
    "orderflow_bias": 1,
    "orderflow_strength": 70,
    "liquidity_signal": 1,
    "liquidity_strength": 70,
}

try:

    final_ai_score = predict_trade_probability(features)

except Exception as e:

    st.error(f"AI ERROR: {e}")

    final_ai_score = 70

signal = generate_signal(trend, "STRONG_BULLISH", final_ai_score, True)

# ==========================================
# AI SIGNAL CARD
# ==========================================

st.subheader("🚨 Current AI Signal")

if signal == "BUY":

    signal_color = "lime"

elif signal == "SELL":

    signal_color = "red"

else:

    signal_color = "orange"

st.markdown(
    f"""
    <h1 style='color:{signal_color};'>
    {signal}
    </h1>
    """,
    unsafe_allow_html=True,
)

st.progress(final_ai_score / 100)

st.write(f"🧠 FINAL AI SCORE: {final_ai_score}%")

# ==========================================
# METRICS
# ==========================================

col1, col2, col3 = st.columns(3)
# TREND
with col1:

    st.write("### TREND")

    if trend == "BULLISH":

        st.success(trend)

    else:

        st.error(trend)

# VOLATILITY
with col2:

    st.write("### VOLATILITY")

    if volatility == "HIGH_VOLATILITY":

        st.warning(volatility)

    else:

        st.success(volatility)

# REGIME
with col3:

    st.write("### REGIME")

    if regime == "TRENDING":

        st.info(regime)

    else:

        st.warning(regime)

# ==========================================
# ORDERFLOW
# ==========================================

st.subheader("🌊 Orderflow")

bias = orderflow["bias"]

if bias == "BUY_PRESSURE":

    st.success(f"Bias: {bias}")

elif bias == "SELL_PRESSURE":

    st.error(f"Bias: {bias}")

else:

    st.warning(f"Bias: {bias}")

st.write(f"Strength: " f"{orderflow['strength']}%")

# ==========================================
# LIQUIDITY
# ==========================================

st.subheader("💧 Liquidity")

liq_signal = liquidity["signal"]

if liq_signal == "BUY_SIDE_SWEEP":

    st.success(liq_signal)

elif liq_signal == "SELL_SIDE_SWEEP":

    st.error(liq_signal)

else:

    st.warning(liq_signal)

# ==========================================
# PRICE DATA
# ==========================================

st.subheader("📈 Market Data")

fig = px.line(df, y="close", title=f"{symbol} Price")

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TRADE HISTORY
# ==========================================

st.subheader("📈 Trade History")

cursor.execute("""
    SELECT
        symbol,
        signal,
        entry,
        sl,
        tp,
        status

    FROM trades

    ORDER BY id DESC

    LIMIT 50
""")

trades = cursor.fetchall()

if trades:

    trades_df = pd.DataFrame(
        trades, columns=["Symbol", "Signal", "Entry", "SL", "TP", "Status"]
    )

    st.dataframe(
        trades_df.style.applymap(
            lambda x: (
                "color: lime"
                if x == "WIN"
                else (
                    "color: red"
                    if x == "LOSS"
                    else ("color: orange" if x == "OPEN" else "")
                )
            ),
            subset=["Status"],
        ),
        use_container_width=True,
    )

else:

    st.write("No trades found")

# ==========================================
# EQUITY CURVE
# ==========================================

st.subheader("📈 Equity Curve")

if len(equity_curve) > 0:

    equity_df = pd.DataFrame(equity_curve, columns=["Balance"])

    equity_fig = px.line(equity_df, y="Balance", title="Portfolio Equity Curve")

    st.plotly_chart(equity_fig, use_container_width=True)

else:

    st.write("No equity data")

# ==========================================
# SIGNAL HISTORY
# ==========================================

st.subheader("🧠 AI Signal History")

cursor.execute("""
    SELECT
        symbol,
        signal,
        probability,
        regime,
        orderflow,
        liquidity

    FROM signals

    ORDER BY id DESC

    LIMIT 50
""")

signals = cursor.fetchall()

if signals:

    signals_df = pd.DataFrame(
        signals,
        columns=["Symbol", "Signal", "Probability", "Regime", "Orderflow", "Liquidity"],
    )

    st.dataframe(
        signals_df.style.applymap(
            lambda x: (
                "color: lime" if x == "BUY" else ("color: red" if x == "SELL" else "")
            ),
            subset=["Signal"],
        ),
        use_container_width=True,
    )

else:

    st.write("No signals found")
