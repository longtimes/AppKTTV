# ===============================
# TRAM MAPPING – DÙNG CHUNG TOÀN DỰ ÁN
# ===============================

TRAM_MAPPING = {

    # ==================================================
    # 🌊 TRẠM MỰC NƯỚC
    # ==================================================
    "mucnuoc": {
        "553000": {
            "ten": "Thành Mỹ",
            "song": "Cái",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553100": {
            "ten": "Hội Khách",
            "song": "Vu Gia",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553300": {
            "ten": "Ái Nghĩa",
            "song": "Vu Gia",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553400": {
            "ten": "Cẩm Lệ",
            "song": "Hàn",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "552600": {
            "ten": "Hiệp Đức",
            "song": "Thu Bồn",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553600": {
            "ten": "Nông Sơn",
            "song": "Thu Bồn",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553200": {
            "ten": "Giao Thủy",
            "song": "Thu Bồn",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "552700": {
            "ten": "Câu Lâu",
            "song": "Thu Bồn",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553700": {
            "ten": "Hội An",
            "song": "Thu Bồn",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
        "553500": {
            "ten": "Tam Kỳ",
            "song": "Tam Kỳ",
            "don_vi": "m",
            "du_an": ["ODAY"],
        },
    },

    # ==================================================
    # ☔ TRẠM ĐO MƯA
    # ==================================================
    "mua": {
        "552800": {
            "ten": "Hiên",
            "lv_song": "Vu Gia",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "552900": {
            "ten": "Khâm Đức",
            "lv_song": "Vu Gia",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553000": {
            "ten": "Thành Mỹ",
            "lv_song": "Vu Gia",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553100": {
            "ten": "Hội Khách",
            "lv_song": "Vu Gia",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553300": {
            "ten": "Ái Nghĩa",
            "lv_song": "Vu Gia",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "558200": {
            "ten": "Hòa Phú",
            "lv_song": "Túy Loan",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553400": {
            "ten": "Cẩm Lệ",
            "lv_song": "Hàn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "556700": {
            "ten": "Trà My",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "558300": {
            "ten": "Tiên Phước",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "552600": {
            "ten": "Hiệp Đức",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553600": {
            "ten": "Nông Sơn",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553200": {
            "ten": "Giao Thủy",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "552700": {
            "ten": "Câu Lâu",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553700": {
            "ten": "Hội An",
            "lv_song": "Thu Bồn",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "553500": {
            "ten": "Kỳ Phú",
            "lv_song": "Tam Kỳ",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
        "556800": {
            "ten": "Tam Kỳ",
            "lv_song": "Tam Kỳ",
            "don_vi": "mm",
            "du_an": ["ODAY"],
        },
    },
}

# ==================================================
# 🔧 HÀM TIỆN ÍCH – DÙNG Ở MỌI NƠI
# ==================================================

def get_ten_tram(matram: str, loai: str = "mucnuoc") -> str:
    """Trả về tên trạm, fallback là mã trạm"""
    return TRAM_MAPPING.get(loai, {}).get(matram, {}).get("ten", matram)


def get_ds_tram(loai: str = "mucnuoc") -> dict:
    """Trả về danh sách trạm theo loại"""
    return TRAM_MAPPING.get(loai, {})


def get_tram_theo_du_an(du_an: str, loai: str = "mucnuoc") -> dict:
    """Lọc trạm theo dự án"""
    return {
        matram: info
        for matram, info in TRAM_MAPPING.get(loai, {}).items()
        if du_an in info.get("du_an", [])
    }
