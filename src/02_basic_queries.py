"""Run TV4 queries 1-3 against campus_graph.lbdb."""
from pathlib import Path
import ladybug as lb

DB_PATH = Path(__file__).resolve().parent / "campus_graph.lbdb"
QUERIES = [
    ("Câu 1 - Điểm LTĐT cao nhất", "MATCH (s:SinhVien)-[h:HOC]->(m:MonHoc) WHERE m.ma_mon = 'LTDT' RETURN s.ma_sv, s.ten, h.diem ORDER BY h.diem DESC LIMIT 1"),
    ("Câu 2 - Điểm trung bình và xếp hạng", "MATCH (s:SinhVien)-[h:HOC]->(m:MonHoc) RETURN s.ma_sv, s.ten, AVG(h.diem) AS diem_trung_binh ORDER BY diem_trung_binh DESC"),
    ("Câu 3 - Sinh viên trượt (điểm < 5)", "MATCH (s:SinhVien)-[h:HOC]->(m:MonHoc) WHERE h.diem < 5.0 RETURN s.ma_sv, s.ten, m.ten_mon, h.diem ORDER BY s.ten, m.ten_mon"),
]

def main():
    if not DB_PATH.exists():
        raise SystemExit("Chưa có campus_graph.lbdb. Chạy 01_setup_db.py trước.")
    db = lb.Database(str(DB_PATH), read_only=True)
    conn = lb.Connection(db)
    try:
        for title, query in QUERIES:
            print(f"\n{title}")
            for row in conn.execute(query):
                print(row)
    finally:
        conn.close()
        db.close()

if __name__ == "__main__":
    main()
