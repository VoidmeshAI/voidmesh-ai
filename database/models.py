# ==========================================
# FILE: database/models.py
# ==========================================

from database.db import cursor, conn

# ==========================================
# SIGNALS TABLE
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        signal TEXT,

        probability REAL,

        regime TEXT,

        orderflow TEXT,

        liquidity TEXT
    )
""")

# ==========================================
# TRADES TABLE
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        signal TEXT,

        entry REAL,

        sl REAL,

        tp REAL,

        status TEXT
    )
""")

conn.commit()

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT
    )
""")

conn.commit()

# ==========================================
# USER PORTFOLIOS
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        balance REAL,

        pnl REAL
    )
""")

conn.commit()


# ==========================================
# USER TRADES
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_trades (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        symbol TEXT,

        signal TEXT,

        entry REAL,

        status TEXT
    )
""")

conn.commit()

# ==========================================
# WINRATE COLUMN
# ==========================================

try:

    cursor.execute("""
        ALTER TABLE portfolios

        ADD COLUMN winrate REAL
""")

except Exception as e:

    print(f"WINRATE COLUMN EXISTS: {e}")

conn.commit()

# ==========================================
# COPY RELATIONSHIPS
# ==========================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS copy_relationships (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        follower TEXT,

        leader TEXT
    )
""")

conn.commit()
