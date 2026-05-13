# ==========================================
# FILE: ai/feature_importance.py
# ==========================================

import joblib

from rich import print


def show_feature_importance():

    # ==========================================
    # LOAD MODEL
    # ==========================================

    model = joblib.load("ai/model.pkl")

    # ==========================================
    # FEATURES
    # ==========================================

    features = [
        "confidence",
        "trend",
        "btc_state",
        "regime",
        "rr",
        "rsi",
        "macd",
        "macd_signal",
        "atr",
        "ema_distance",
        "volume_spike",
    ]

    # ==========================================
    # IMPORTANCE
    # ==========================================

    importance = model.feature_importances_

    ranked = sorted(zip(features, importance), key=lambda x: x[1], reverse=True)

    # ==========================================
    # REPORT
    # ==========================================

    print("\n[bold cyan]" "AI FEATURE IMPORTANCE" "[/bold cyan]")

    for feature, score in ranked:

        print(f"{feature}: " f"{round(score * 100, 2)}%")
