import sqlite3
from flask import g

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("Credentials.db")
    return db

def close_db(exception = None):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def exec(query, params=()):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query,params)
    db.commit()
    return cursor

def fetch(query, params=()):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS Credentials(
                        FullName TEXT,
                        age TEXT)""")
        db.commit()