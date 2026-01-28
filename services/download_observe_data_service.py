import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

# import nội bộ trong package services
from .db_service import lay_thoi_gian_cuoi

# ===============================
# Thư mục dự án & lưu dữ liệu
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "download"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# Danh sách trạm
# ===============================
TRAM = {
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

# ===============================
# Parse datetime an toàn
# ===============================
def parse_datetime_safe(s: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Không parse được datetime: {s}")

# ===============================
# Tạo link API
# ===============================
def tao_link_api(matram, tgbd, tgkt):
    return (
        "http://203.209.181.170:2018/API_TTB/json/solieu.php"
        f"?matram={matram}"
        "&ten_table=mucnuoc_oday"
        "&sophut=60"
        "&tinhtong=0"
        f"&thoigianbd='{tgbd}'"
        f"&thoigiankt='{tgkt}'"
    )

# ===============================
# Tải 1 trạm
# ===============================
def tai_1_tram(matram, tentram, tgbd, tgkt) -> int:
    url = tao_link_api(matram, tgbd, tgkt)
    print(f"\n📡 {tentram} ({matram})")
    print("🔗", url)

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()

        if not data:
            print("⚠️ Không có dữ liệu mới")
            return 0

        filename = f"{matram}_{tgbd.replace(':','')}_{tgkt.replace(':','')}.json"
        filepath = DATA_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Lưu {len(data)} bản ghi")
        return len(data)

    except Exception as e:
        print(f"❌ Lỗi trạm {matram}: {e}")
        return 0

# ===============================
# Tải toàn bộ trạm (CHO STREAMLIT)
# ===============================
def tai_tat_ca_tram():
    try:
        # 1️⃣ Lấy thời gian cuối trong DB
        tg_cuoi = lay_thoi_gian_cuoi()

        if tg_cuoi:
            tgbd = parse_datetime_safe(tg_cuoi) + timedelta(hours=1)
            print(f"📌 DB đã có dữ liệu đến: {tg_cuoi}")
        else:
            tgbd = datetime(2025, 1, 1, 0, 0)
            print("📌 DB chưa có dữ liệu, tải từ đầu")

        tgkt = datetime.now()

        tgbd_str = tgbd.strftime("%Y-%m-%d %H:%M")
        tgkt_str = tgkt.strftime("%Y-%m-%d %H:%M")

        print(f"⏱️ Khoảng tải: {tgbd_str} → {tgkt_str}")

        # 2️⃣ Tải từng trạm
        tong = 0
        for matram, tentram in TRAM.items():
            tong += tai_1_tram(matram, tentram, tgbd_str, tgkt_str)

        # 3️⃣ TRẢ KẾT QUẢ CHO UI
        return True, f"🎉 Hoàn thành tải {tong} bản ghi cho {len(TRAM)} trạm"

    except Exception as e:
        return False, f"❌ Lỗi khi tải dữ liệu: {e}"

# ===============================
# Chạy độc lập (test)
# ===============================
if __name__ == "__main__":
    ok, msg = tai_tat_ca_tram()
    print(msg)
