# ==========================================
# FILE: api/main.py
# ==========================================

import database.models

from fastapi import FastAPI, Form, WebSocket

from auth.auth import hash_password, verify_password, create_access_token

from database.db import cursor

from papertrade.portfolio import portfolio

from dashboard_utils.heatmap_data import generate_heatmap

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# ROOT
# ==========================================


@app.get("/")
def root():

    return {"message": "VOIDMESH AI API RUNNING"}


# ==========================================
# PORTFOLIO
# ==========================================


@app.get("/portfolio")
def get_portfolio():

    return portfolio


# ==========================================
# SIGNALS
# ==========================================


@app.get("/signals")
def get_signals():

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

        LIMIT 20
""")

    signals = cursor.fetchall()

    return {"signals": signals}


# ==========================================
# TRADES
# ==========================================


@app.get("/trades")
def get_trades():

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

        LIMIT 20
""")

    trades = cursor.fetchall()

    return {"trades": trades}


# ==========================================
# HEATMAP
# ==========================================


@app.get("/heatmap")
def get_heatmap():

    heatmap = generate_heatmap()

    return {"heatmap": heatmap}


# ==========================================
# WEBSOCKET
# ==========================================


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:

        data = {
            "balance": portfolio["current_balance"],
            "pnl": portfolio["realized_pnl"],
            "growth": round(
                (
                    (portfolio["current_balance"] - portfolio["starting_balance"])
                    / portfolio["starting_balance"]
                )
                * 100,
                2,
            ),
        }

        await websocket.send_json(data)

        import asyncio

        await asyncio.sleep(2)


# ==========================================
# SIGNUP
# ==========================================


@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...)):

    hashed = hash_password(password)

    try:

        cursor.execute(
            """
            INSERT INTO users (

                username,
                password

            )

            VALUES (?, ?)
            """,
            (username, hashed),
        )

        conn.commit()

        cursor.execute(
            """
            INSERT INTO portfolios (

                username,
                balance,
                pnl

            )

            VALUES (?, ?, ?)
            """,
            (username, 1000, 0),
        )

        conn.commit()

        return {"message": "USER CREATED"}

    except Exception as e:

        return {"error": str(e)}


# ==========================================
# LOGIN
# ==========================================


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    cursor.execute(
        """
        SELECT password

        FROM users

        WHERE username = ?
""",
        (username,),
    )

    user = cursor.fetchone()

    if not user:

        return {"error": "INVALID USER"}

    hashed_password = user[0]

    valid = verify_password(password, hashed_password)

    if not valid:

        return {"error": "INVALID PASSWORD"}

    token = create_access_token({"sub": username})

    return {"access_token": token}


# ==========================================
# USER PORTFOLIO
# ==========================================


@app.get("/user/{username}/portfolio")
def get_user_portfolio(username: str):

    cursor.execute(
        """
        SELECT
            balance,
            pnl

        FROM portfolios

        WHERE username = ?
""",
        (username,),
    )

    portfolio = cursor.fetchone()

    if not portfolio:

        return {"error": "USER NOT FOUND"}

    return {"username": username, "balance": portfolio[0], "pnl": portfolio[1]}


# ==========================================
# SAVE USER TRADE
# ==========================================


@app.post("/user/{username}/trade")
def save_user_trade(
    username: str,
    symbol: str = Form(...),
    signal: str = Form(...),
    entry: float = Form(...),
):

    cursor.execute(
        """
        INSERT INTO user_trades (

            username,
            symbol,
            signal,
            entry,
            status

        )

        VALUES (?, ?, ?, ?, ?)
""",
        (username, symbol, signal, entry, "OPEN"),
    )

    conn.commit()

    return {"message": "TRADE SAVED"}


# ==========================================
# USER TRADES
# ==========================================


@app.get("/user/{username}/trades")
def get_user_trades(username: str):

    cursor.execute(
        """
        SELECT
            symbol,
            signal,
            entry,
            status

        FROM user_trades

        WHERE username = ?

        ORDER BY id DESC
""",
        (username,),
    )

    trades = cursor.fetchall()

    return {"trades": trades}


# ==========================================
# LEADERBOARD
# ==========================================


@app.get("/leaderboard")
def get_leaderboard():

    cursor.execute("""
        SELECT
            username,
            balance,
            pnl,
            winrate

        FROM portfolios

        ORDER BY pnl DESC

        LIMIT 20
""")

    leaderboard = cursor.fetchall()

    return {"leaderboard": leaderboard}


# ==========================================
# FOLLOW LEADER
# ==========================================


@app.post("/follow")
def follow_leader(follower: str = Form(...), leader: str = Form(...)):

    cursor.execute(
        """
        INSERT INTO copy_relationships (

            follower,
            leader

        )

        VALUES (?, ?)
""",
        (follower, leader),
    )

    conn.commit()

    return {"message": "FOLLOWING STARTED"}


# ==========================================
# GET FOLLOWERS
# ==========================================


@app.get("/followers/{leader}")
def get_followers(leader: str):

    cursor.execute(
        """
        SELECT follower

        FROM copy_relationships

        WHERE leader = ?
""",
        (leader,),
    )

    followers = cursor.fetchall()

    return {"followers": followers}
