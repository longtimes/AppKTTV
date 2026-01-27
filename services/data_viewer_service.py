import sqlite3
import pandas as pd
from pathlib import Path

# ======================================================
# CẤU HÌNH DATABASE
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "observe_data.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ======================================================
# LOAD DỮ LIỆU
# ======================================================
def load_solieu():
    conn = get_connection()
    df = pd.read_sql(
        "SELECT matram, Thoigian_SL, Solieu FROM solieu",
        conn
    )
    conn.close()
    return df


# ======================================================
# UPDATE DỮ LIỆU
# ======================================================
def update_solieu(df: pd.DataFrame):
    """
    Cập nhật giá trị Solieu theo khóa chính (matram, Thoigian_SL)
    """
    if df.empty:
        return

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            UPDATE solieu
            SET Solieu = ?
            WHERE matram = ?
              AND Thoigian_SL = ?
            """,
            (
                float(row["Solieu"]),
                row["matram"],
                row["Thoigian_SL"]
            )
        )

    conn.commit()
    conn.close()


# ======================================================
# DELETE DỮ LIỆU
# ======================================================
def delete_solieu(df: pd.DataFrame):
    """
    Xóa dữ liệu theo khóa chính (matram, Thoigian_SL)
    """
    if df.empty:
        return

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            DELETE FROM solieu
            WHERE matram = ?
              AND Thoigian_SL = ?
            """,
            (
                row["matram"],
                row["Thoigian_SL"]
            )
        )

    conn.commit()
    conn.close()
