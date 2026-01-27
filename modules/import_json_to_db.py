import json
import sqlite3
from pathlib import Path
import glob

# ===============================
# Đường dẫn
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "download"
DB_PATH = BASE_DIR / "data" / "observe_data.db"

# ===============================
# Kết nối CSDL
# ===============================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ===============================
# SQL insert
# ===============================
sql = """
INSERT OR IGNORE INTO mucnuoc_oday (ma_tram, thoi_gian, gia_tri)
VALUES (?, ?, ?)
"""

# ===============================
# Đọc tất cả file JSON
# ===============================
files = sorted(DATA_DIR.glob("*.json"))

tong = 0
for file in files:
    print(f"📂 Đang xử lý: {file.name}")

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dem_file = 0
    for item in data:
        try:
            ma_tram = item["matram"]
            thoi_gian = item["Thoigian_SL"]
            gia_tri = float(item["Solieu"])

            cursor.execute(sql, (ma_tram, thoi_gian, gia_tri))
            dem_file += 1
        except Exception as e:
            print(f"⚠️ Bỏ qua bản ghi lỗi: {e}")

    conn.commit()
    print(f"   ✅ Đã xử lý {dem_file} dòng")

    tong += dem_file

cursor.close()
conn.close()

print(f"\n🎉 Hoàn tất! Tổng số bản ghi xử lý: {tong}")
