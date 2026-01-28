# ===============================
# TRAM MAPPING – DÙNG CHUNG TOÀN DỰ ÁN
# ===============================

TRAM_MAPPING = {
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
            "du_an": ["TTB"],
        },
    }
}

# ===============================
# HÀM TIỆN ÍCH (NÊN DÙNG)
# ===============================

def get_ten_tram(matram: str, loai: str = "mucnuoc") -> str:
    """
    Trả về tên trạm theo mã trạm
    """
    return TRAM_MAPPING.get(loai, {}).get(matram, {}).get("ten", matram)


def get_ds_tram(loai: str = "mucnuoc") -> dict:
    """
    Trả về toàn bộ danh sách trạm theo loại
    """
    return TRAM_MAPPING.get(loai, {})


def get_tram_theo_du_an(du_an: str, loai: str = "mucnuoc") -> dict:
    """
    Lọc trạm theo dự án
    """
    return {
        matram: info
        for matram, info in TRAM_MAPPING.get(loai, {}).items()
        if du_an in info.get("du_an", [])
    }
