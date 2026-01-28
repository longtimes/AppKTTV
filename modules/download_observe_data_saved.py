import streamlit as st
from services.download_observe_data_service import tai_tat_ca_tram

def run():
    st.header("📥 Tải dữ liệu quan trắc mực nước")

    st.markdown("Nhập thời gian theo định dạng: `YYYY-MM-DD HH:MM`")

    col1, col2 = st.columns(2)
    with col1:
        tgbd = st.text_input("⏱️ Thời gian bắt đầu", "2025-01-01 00:00")
    with col2:
        tgkt = st.text_input("⏱️ Thời gian kết thúc", "2025-01-02 00:00")

    if st.button("🚀 Tải dữ liệu", use_container_width=True):
        with st.spinner("Đang tải dữ liệu từ API KTTV..."):
            ket_qua = tai_tat_ca_tram(tgbd, tgkt)

        st.success("✅ Hoàn thành tải dữ liệu")
