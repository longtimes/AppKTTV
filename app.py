import streamlit as st

# ===============================
# Cấu hình ứng dụng
# ===============================
st.set_page_config(
    page_title="Phần mềm hỗ trợ KTTV",
    layout="wide",
)

# ===============================
# Sidebar
# ===============================
st.sidebar.title("☁️ HỖ TRỢ KTTV")

menu = st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "Tổng quan",
        "Tải dữ liệu quan trắc",
        "Import dữ liệu vào CSDL",
        "Xem dữ liệu",
    ]
)

# ===============================
# Điều hướng module
# ===============================
if menu == "Tổng quan":
    from modules.dashboard import run
    run()

elif menu == "Tải dữ liệu quan trắc":
    from modules.download_observe_data import run
    run()

elif menu == "Import dữ liệu vào CSDL":
    from modules.import_json_to_db import run
    run()

elif menu == "Xem dữ liệu":
    from modules.data_viewer import run
    run()
