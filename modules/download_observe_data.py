import streamlit as st
from services.download_observe_data_service import tai_tat_ca_tram

def run():
    st.header("📥 Tải dữ liệu quan trắc mực nước")

    st.markdown(
        "Hệ thống sẽ **tự động tải dữ liệu từ thời điểm có số liệu gần nhất trong DB** "
        "đến **thời điểm hiện tại**."
    )

    if st.button("🚀 Tải dữ liệu", use_container_width=True):
        with st.spinner("Đang tải dữ liệu từ API KTTV..."):
            ok, msg = tai_tat_ca_tram()

        if ok:
            st.success(msg)
        else:
            st.error(msg)
