import sqlite3
from pathlib import Path

# Thư mục gốc app/
BASE_DIR = Path(__file__).resolve().parent.parent

# Thư mục data
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# File CSDL
DB_PATH = DATA_DIR / "observe_data.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Bảng danh mục trạm (ma_tram là PRIMARY KEY)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        ma_tram TEXT PRIMARY KEY,
        ten_tram TEXT,
        tab TEXT,
        yeu_to TEXT,
        loai_tram TEXT,
        du_an TEXT,
        tinh TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Đã tạo bảng stations với PRIMARY KEY = ma_tram")
    print("DB:", DB_PATH)
