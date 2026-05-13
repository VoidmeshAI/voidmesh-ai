import json
import os

DB_FILE = "database/trades.json"


def save_trade(data):

    # Create file if missing
    if not os.path.exists(DB_FILE):

        with open(DB_FILE, "w") as f:
            json.dump([], f)

    # Load existing trades safely
    try:

        with open(DB_FILE, "r") as f:
            trades = json.load(f)

    except:

        trades = []

    # Append new trade
    trades.append(data)

    # Save updated trades
    with open(DB_FILE, "w") as f:
        json.dump(trades, f, indent=4)