import sqlite3
from pathlib import Path

# ===============================
# Thư mục gốc app/
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

# Thư mục data/
DATA_DIR = BASE_DIR / "D:/DEV/app/data"
DATA_DIR.mkdir(exist_ok=True)

# File CSDL
DB_PATH = DATA_DIR / "observe_data.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ===============================
    # Bảng dữ liệu thô (GIỐNG JSON)
    # ===============================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS solieu (
        matram TEXT NOT NULL,
        Thoigian_SL TEXT NOT NULL,
        Solieu REAL,
        PRIMARY KEY (matram, Thoigian_SL)
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Đã tạo CSDL observe_data.db")
    print("✅ Đã tạo bảng solieu (matram, Thoigian_SL, Solieu)")
    print("📁 DB:", DB_PATH)
