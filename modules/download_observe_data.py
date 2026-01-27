import requests
import json
from pathlib import Path
from datetime import datetime

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
# Tạo link API (đúng chuẩn của bạn)
# ===============================
def tao_link_api(matram, tgbd, tgkt):
    return (
        "http://203.209.181.170:2018/API_TTB/json/solieu.php"
        f"?matram={matram}"
        "&ten_table=mucnuoc_oday"
        "&sophut=10"
        "&tinhtong=0"
        f"&thoigianbd='{tgbd}'"
        f"&thoigiankt='{tgkt}'"
    )

# ===============================
# Tải 1 trạm
# ===============================
def tai_1_tram(matram, tentram, tgbd, tgkt):
    url = tao_link_api(matram, tgbd, tgkt)
    print(f"\n📡 Trạm {matram} – {tentram}")
    print("🔗", url)

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()

        if not data:
            print("⚠️ Không có dữ liệu")
            return

        filename = f"{matram}_{tgbd.replace(':','')}_{tgkt.replace(':','')}.json"
        filepath = DATA_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Lưu {len(data)} bản ghi → {filepath.name}")

    except Exception as e:
        print(f"❌ Lỗi trạm {matram}: {e}")

# ===============================
# Tải toàn bộ trạm
# ===============================
def tai_tat_ca_tram(tgbd, tgkt):
    print("🚀 Bắt đầu tải dữ liệu")
    print(f"⏱️ Thời gian: {tgbd} → {tgkt}")

    for matram, tentram in TRAM.items():
        tai_1_tram(matram, tentram, tgbd, tgkt)

    print("\n🎉 Hoàn thành tải dữ liệu cho tất cả trạm")

# ===============================
# Chạy độc lập
# ===============================
if __name__ == "__main__":
    tai_tat_ca_tram(
        tgbd="2025-01-01 00:00",
        tgkt="2025-01-02 00:00"
    )
