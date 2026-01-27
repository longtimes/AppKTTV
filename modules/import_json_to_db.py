import streamlit as st
from services.import_json_to_db_service import import_to_db
def run():
    st.header("🗄️ Import dữ liệu vào CSDL")

    if st.button("📥 Import dữ liệu"):
        with st.spinner("Đang import dữ liệu vào DB..."):
            ok, msg = import_to_db()

        if ok:
            st.success(msg)
        else:
            st.error("❌ Import thất bại")
            st.code(msg)
