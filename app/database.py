import sqlite3


def get_db():
    conn = sqlite3.connect("leads.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    with app.app_context():
        conn = get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()


def lead_ekle(isim, telefon, mesaj):
    conn = get_db()
    conn.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )
    conn.commit()
    conn.close()


def tum_leadler():
    conn = get_db()
    leads = conn.execute(
        "SELECT * FROM leads ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return leads