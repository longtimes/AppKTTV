import sqlite3
from pathlib import Path

# ====== ĐƯỜNG DẪN FILE DB ======
db_path = Path("D:/DEV/app/data/observe_data.db")   # 🔴 sửa đúng đường dẫn của bạn

if not db_path.exists():
    print("❌ Không tìm thấy file DB:", db_path)
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n📌 DANH SÁCH CÁC BẢNG TRONG DATABASE:\n")

cursor.execute("""
    SELECT name 
    FROM sqlite_master 
    WHERE type='table'
""")

tables = cursor.fetchall()

if not tables:
    print("⚠️ Database chưa có bảng nào")
else:
    for (table_name,) in tables:
        print(f"🗂 Bảng: {table_name}")

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            cid, name, col_type, notnull, default, pk = col
            print(f"   - {name} ({col_type}) {'[PK]' if pk else ''}")

        print("-" * 40)

conn.close()
