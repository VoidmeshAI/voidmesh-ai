# ==========================================
# FILE: copytrading/copier.py
# ==========================================

from rich import print

from database.db import cursor, conn


def copy_trade(leader, symbol, signal, entry):

    # ==========================================
    # GET FOLLOWERS
    # ==========================================

    cursor.execute(
        """
        SELECT follower

        FROM copy_relationships

        WHERE leader = ?
""",
        (leader,),
    )

    followers = cursor.fetchall()

    # ==========================================
    # COPY TRADES
    # ==========================================

    for follower in followers:

        username = follower[0]

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

        print(f"\n[bold green]" f"TRADE COPIED TO:" f"[/bold green] " f"{username}")
