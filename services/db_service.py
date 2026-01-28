import sqlite3
from pathlib import Path

# ===============================
# Đường dẫn DB
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "observe_data.db"

# ===============================
# Lấy thời gian số liệu mới nhất
# ===============================
def lay_thoi_gian_cuoi(matram=None):
    """
    Trả về thời gian quan trắc mới nhất trong DB
    Nếu có matram → lấy theo trạm
    Nếu không → lấy toàn DB
    """

    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if matram:
        cur.execute(
            "SELECT MAX(Thoigian_SL) FROM solieu WHERE matram = ?",
            (matram,)
        )
    else:
        cur.execute(
            "SELECT MAX(Thoigian_SL) FROM solieu"
        )

    result = cur.fetchone()[0]
    conn.close()

    return result
