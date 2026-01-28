import json
import sqlite3
from pathlib import Path
import glob

# ===============================
# Cấu hình đường dẫn
# ===============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JSON_DIR = DATA_DIR / "download"
DB_PATH = DATA_DIR / "observe_data.db"


# ===============================
# Kết nối DB
# ===============================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ===============================
# Import 1 file JSON
# ===============================

def import_one_json(json_path: Path) -> int:
    print(f"📂 Đang xử lý: {json_path.name}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("⚠️ File không phải danh sách JSON")
        return 0

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT OR IGNORE INTO solieu (matram, Thoigian_SL, Solieu)
        VALUES (?, ?, ?)
    """

    rows = []
    for item in data:
        try:
            matram = item["matram"]
            thoigian = item["Thoigian_SL"]
            solieu = float(item["Solieu"]) if item["Solieu"] is not None else None
            rows.append((matram, thoigian, solieu))
        except KeyError as e:
            print(f"⚠️ Thiếu key {e} trong file {json_path.name}")

    cur.executemany(sql, rows)
    conn.commit()
    conn.close()

    print(f"✅ Đã import {len(rows)} dòng\n")
    return len(rows)


# ===============================
# Import toàn bộ thư mục (logic lõi)
# ===============================

def import_all() -> int:
    if not JSON_DIR.exists():
        raise FileNotFoundError(f"Không tồn tại thư mục {JSON_DIR}")

    json_files = list(JSON_DIR.glob("*.json"))

    if not json_files:
        raise FileNotFoundError("Không có file JSON nào trong thư mục download")

    total = 0
    for file_path in json_files:
        total += import_one_json(file_path)

    print(f"🎉 HOÀN THÀNH – Tổng dòng xử lý: {total}")
    return total


# ===============================
# HÀM DÙNG CHO STREAMLIT (QUAN TRỌNG)
# ===============================

def import_to_db():
    """
    Hàm adapter cho Streamlit
    BẮT BUỘC return (ok, message)
    """
    try:
        total = import_all()
        return True, f"Đã import thành công {total} dòng dữ liệu"
    except Exception as e:
        return False, str(e)


# ===============================
# Chạy trực tiếp (CLI)
# ===============================

if __name__ == "__main__":
    total = import_all()
    print(f"IMPORT XONG – {total} dòng")
