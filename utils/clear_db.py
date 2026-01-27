import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "observe_data.db"

def clear_all_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM solieu;")
    conn.commit()
    conn.close()

    print("✅ Đã xóa toàn bộ dữ liệu trong bảng solieu")

if __name__ == "__main__":
    clear_all_data()
