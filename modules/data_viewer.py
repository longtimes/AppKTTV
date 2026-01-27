import streamlit as st
import pandas as pd
from services.data_viewer_service import load_solieu


def run():
    st.header("📊 Số liệu quan trắc")

    df = load_solieu()

    if df.empty:
        st.warning("⚠️ Bảng solieu chưa có dữ liệu")
        return

    # ---- xử lý thời gian ----
    df["Thoigian_SL"] = pd.to_datetime(df["Thoigian_SL"], errors="coerce")
    df = df.dropna(subset=["Thoigian_SL"])
    df = df.sort_values("Thoigian_SL")

    # ---- chọn trạm ----
    tram_list = sorted(df["matram"].unique())
    tram_chon = st.multiselect(
        "📍 Chọn trạm",
        tram_list,
        default=tram_list[:1]
    )

    if tram_chon:
        df = df[df["matram"].isin(tram_chon)]

    # ---- chọn khoảng thời gian ----
    min_date = df["Thoigian_SL"].min().date()
    max_date = df["Thoigian_SL"].max().date()

    col1, col2 = st.columns(2)
    with col1:
        tu_ngay = st.date_input("📅 Từ ngày", min_date)
    with col2:
        den_ngay = st.date_input("📅 Đến ngày", max_date)

    df = df[
        (df["Thoigian_SL"].dt.date >= tu_ngay) &
        (df["Thoigian_SL"].dt.date <= den_ngay)
    ]

    st.divider()

    # ---- thống kê nhanh ----
    c1, c2, c3 = st.columns(3)
    c1.metric("📄 Số bản ghi", len(df))
    c2.metric("📍 Số trạm", df["matram"].nunique())
    c3.metric("⏱ Khoảng TG", f"{tu_ngay} → {den_ngay}")

    # ---- biểu đồ ----
    st.subheader("📈 Biểu đồ theo thời gian")
    st.line_chart(
        df,
        x="Thoigian_SL",
        y="Solieu",
        color="matram"
    )

    # ---- bảng dữ liệu ----
    st.subheader("📋 Bảng số liệu")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ---- tải CSV ----
    st.download_button(
        "⬇️ Tải dữ liệu CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="solieu_loc.csv",
        mime="text/csv"
    )
