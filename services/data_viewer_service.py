import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "observe_data.db"


def load_solieu():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM solieu", conn)
    conn.close()
    return df
