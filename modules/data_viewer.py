import streamlit as st
import pandas as pd
from services.data_viewer_service import (
    load_solieu,
    update_solieu,
    delete_solieu
)


def run():
    st.header("📊 Số liệu quan trắc")

    # ======================================================
    # LOAD DỮ LIỆU
    # ======================================================
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
    # BIỂU ĐỒ
    # ======================================================
    st.subheader("📈 Biểu đồ theo thời gian")
    st.line_chart(
        df,
        x="Thoigian_SL",
        y="Solieu",
        color="matram",
        height=450
    )

    st.divider()

    # ======================================================
    # CHỈNH SỬA DỮ LIỆU
    # ======================================================
    st.subheader("✏️ Chỉnh sửa số liệu (có thể sửa & xóa)")

    df_edit = df.copy()
    df_edit["Xóa"] = False

    edited_df = st.data_editor(
        df_edit,
        use_container_width=True,
        hide_index=True,
        column_config={
            "matram": st.column_config.TextColumn(
                "Trạm", disabled=True
            ),
            "Thoigian_SL": st.column_config.DatetimeColumn(
                "Thời gian", disabled=True
            ),
            "Solieu": st.column_config.NumberColumn(
                "Số liệu", step=0.01
            ),
            "Xóa": st.column_config.CheckboxColumn("Xóa")
        },
        key="editor"
    )

    # ======================================================
    # KHỞI TẠO SESSION STATE
    # ======================================================
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    # ======================================================
    # NÚT LƯU
    # ======================================================
    if st.button("💾 Lưu thay đổi vào CSDL", type="primary"):
        df_delete = edited_df[edited_df["Xóa"] == True]
        df_update = edited_df[edited_df["Xóa"] == False]

        if not df_delete.empty:
            st.session_state.confirm_delete = True
            st.session_state.df_delete = df_delete.copy()
            st.session_state.df_update = df_update.copy()
        else:
            df_update["Thoigian_SL"] = df_update["Thoigian_SL"].dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            update_solieu(df_update)
            st.success("✅ Đã cập nhật dữ liệu vào CSDL")
            st.rerun()

    # ======================================================
    # CONFIRM XÓA
    # ======================================================
    if st.session_state.confirm_delete:
        st.warning(
            "⚠️ Bạn sắp **XÓA DỮ LIỆU** khỏi CSDL. "
            "Hành động này KHÔNG thể hoàn tác!"
        )

        st.dataframe(
            st.session_state.df_delete[
                ["matram", "Thoigian_SL", "Solieu"]
            ],
            use_container_width=True,
            hide_index=True
        )

        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("🗑️ Xác nhận xóa", type="primary"):
                df_del = st.session_state.df_delete
                df_upd = st.session_state.df_update

                df_del["Thoigian_SL"] = df_del["Thoigian_SL"].dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                df_upd["Thoigian_SL"] = df_upd["Thoigian_SL"].dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                update_solieu(df_upd)
                delete_solieu(df_del)

                st.session_state.confirm_delete = False
                st.success("✅ Đã xóa và cập nhật dữ liệu vào CSDL")
                st.rerun()

        with col_no:
            if st.button("❌ Hủy"):
                st.session_state.confirm_delete = False
                st.info("Đã hủy thao tác xóa")
                st.rerun()
