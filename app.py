import streamlit as st

st.set_page_config(
    page_title="Phần mềm hỗ trợ KTTV",
    layout="wide"
)

st.sidebar.title("☁️ HỖ TRỢ KTTV")

module = st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "Tổng quan",
        "Tải dữ liệu"
    ]
)

if module == "Tổng quan":
    from modules.dashboard import run
    run()

elif module == "Tải dữ liệu":
    from modules.data_viewer import run
    run()
