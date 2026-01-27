import streamlit as st
import pandas as pd
from services.data_viewer_service import load_solieu


def run():
    st.header("📊 Số liệu quan trắc")

    df = load_solieu()

    if df.empty:
        st.warning("⚠️ Bảng solieu chưa có dữ liệu")
        return

    # ======================================================
    # XỬ LÝ THỜI GIAN
    # ======================================================
    df["Thoigian_SL"] = pd.to_datetime(df["Thoigian_SL"], errors="coerce")
    df = df.dropna(subset=["Thoigian_SL"])
    df = df.sort_values("Thoigian_SL")

    # ======================================================
    # CHỌN TRẠM
    # ======================================================
    tram_list = sorted(df["matram"].unique())
    tram_chon = st.multiselect(
        "📍 Chọn trạm",
        tram_list,
        default=tram_list[:1]
    )

    if tram_chon:
        df = df[df["matram"].isin(tram_chon)]

    # ======================================================
    # CHỌN KHOẢNG THỜI GIAN
    # ======================================================
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

    # ======================================================
    # BIỂU ĐỒ (ƯU TIÊN HIỂN THỊ)
    # ======================================================
    st.subheader("📈 Biểu đồ theo thời gian")
    st.line_chart(
        df,
        x="Thoigian_SL",
        y="Solieu",
        color="matram",
        height=450   # 👈 tăng kích thước biểu đồ
    )

    # ======================================================
    # METRIC (THU NHỎ – GỌN)
    # ======================================================
    st.markdown("""
    <style>
    .stat-box {
        padding: 10px;
        border-radius: 8px;
        background-color: #f6f7f9;
        text-align: center;
    }
    .stat-title {
        font-size: 14px;
        color: #555;
    }
    .stat-value {
        font-size: 22px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-title">📄 Số bản ghi</div>
                <div class="stat-value">{len(df)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-title">📍 Số trạm</div>
                <div class="stat-value">{df["matram"].nunique()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-title">⏱ Khoảng thời gian</div>
                <div class="stat-value">{tu_ngay} → {den_ngay}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ======================================================
    # BẢNG DỮ LIỆU
    # ======================================================
    st.subheader("📋 Bảng số liệu")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================================
    # TẢI CSV
    # ======================================================
    st.download_button(
        "⬇️ Tải dữ liệu CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="solieu_loc.csv",
        mime="text/csv"
    )
