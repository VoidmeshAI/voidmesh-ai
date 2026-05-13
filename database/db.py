# ==========================================
# FILE: database/db.py
# ==========================================

import sqlite3

# ==========================================
# CONNECT
# ==========================================

conn = sqlite3.connect("voidmesh.db", check_same_thread=False)

cursor = conn.cursor()
