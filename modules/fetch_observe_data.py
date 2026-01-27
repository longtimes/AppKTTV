import requests
import sqlite3
from pathlib import Path
from urllib.parse import quote

# ==================================
# CẤU HÌNH
# ==================================

API_BASE = "http://203.209.181.170:2018/API_TTB/json/solieu.php"

DB_PATH = Path(__file__).parent / "observe_data.db"

# Danh sách trạm (từ HTML của bạn)
STATIONS = {
    "553000": "Thành Mỹ",
    "553100": "Hội Khách",
    "553300": "Ái Nghĩa",
    "553400": "Cẩm Lệ",
    "552600": "Hiệp Đức",
    "553600": "Nông Sơn",
    "553200": "Giao Thủy",
    "552700": "Câu Lâu",
    "553700": "Hội An",
    "553500": "Tam Kỳ",
}

# ==================================
# KHỞI TẠO CSDL
# ==================================

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Bảng trạm
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                ma_tram TEXT PRIMARY KEY,
                ten_tram TEXT
            )
        """)

        # Bảng mực nước
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mucnuoc_oday (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_tram TEXT NOT NULL,
                thoi_gian TEXT NOT NULL,
                gia_tri REAL,
                UNIQUE (ma_tram, thoi_gian)
            )
        """)

        # Ghi danh mục trạm
        cursor.executemany(
            "INSERT OR IGNORE INTO stations (ma_tram, ten_tram) VALUES (?, ?)",
            [(k, v) for k, v in STATIONS.items()]
        )

# ==================================
# LẤY DỮ LIỆU TỪ API
# ==================================

def fetch_data_from_api(ma_tram, thoigianbd, thoigiankt):
    url = (
        f"{API_BASE}"
        f"?matram={ma_tram}"
        f"&ten_table=mucnuoc_oday"
        f"&sophut=10"
        f"&tinhtong=0"
        f"&thoigianbd={quote(thoigianbd)}"
        f"&thoigiankt={quote(thoigiankt)}"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Lỗi API trạm {ma_tram}: {e}")
        return []

# ==================================
# GHI DỮ LIỆU VÀO CSDL
# ==================================

def insert_data(ma_tram, data):
    sql = """
        INSERT OR IGNORE INTO mucnuoc_oday
        (ma_tram, thoi_gian, gia_tri)
        VALUES (?, ?, ?)
    """

    rows = []
    for item in data:
        thoi_gian = item.get("thoigian")
        gia_tri = item.get("giatri")

        if thoi_gian is None or gia_tri is None:
            continue

        rows.append((ma_tram, thoi_gian, gia_tri))

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany(sql, rows)

    return len(rows)

# ==================================
# CHẠY LẤY & LƯU DỮ LIỆU
# ==================================

def run_all_stations(thoigianbd, thoigiankt):
    init_db()

    for ma_tram, ten_tram in STATIONS.items():
        print(f"📡 Đang lấy dữ liệu: {ten_tram} ({ma_tram})")

        data = fetch_data_from_api(ma_tram, thoigianbd, thoigiankt)

        if not data:
            print("   ⚠️ Không có dữ liệu")
            continue

        count = insert_data(ma_tram, data)
        print(f"   ✅ Đã lưu {count} bản ghi")

# ==================================
# CHẠY TRỰC TIẾP
# ==================================

if __name__ == "__main__":
    run_all_stations(
        thoigianbd="2025-01-01 00:00",
        thoigiankt="2025-01-02 00:00"
    )
