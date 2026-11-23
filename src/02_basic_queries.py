"""Chạy ba truy vấn cơ bản được phân công cho TV4."""
from pathlib import Path

import ladybug as lb


DUONG_DAN_DB = Path(__file__).resolve().parent / "campus_graph.lbdb"

TRUY_VAN = [
    (
        "Câu 1 - Sinh viên có điểm LTĐT cao nhất",
        """MATCH (s:SinhVien)-[h:HOC]->(m:MonHoc)
        WHERE m.ma_mon = $ma_mon
        RETURN s.ma_sv AS ma_sv, s.ten AS ten_sinh_vien,
               h.diem AS diem
        ORDER BY diem DESC
        LIMIT 1""",
        {"ma_mon": "LTDT"},
    ),
    (
        "Câu 2 - Điểm trung bình và xếp hạng",
        """MATCH (s:SinhVien)-[h:HOC]->(m:MonHoc)
        RETURN s.ma_sv AS ma_sv, s.ten AS ten_sinh_vien,
               ROUND(AVG(h.diem), 2) AS diem_trung_binh
        ORDER BY diem_trung_binh DESC, s.ma_sv""",
        {},
    ),
    (
        "Câu 3 - Sinh viên trượt môn (điểm dưới 5)",
        """MATCH (s:SinhVien)-[h:HOC]->(m:MonHoc)
        WHERE h.diem < 5.0
        RETURN s.ma_sv AS ma_sv, s.ten AS ten_sinh_vien,
               m.ten_mon AS ten_mon_hoc, h.diem AS diem
        ORDER BY s.ten, m.ten_mon""",
        {},
    ),
]


def in_ket_qua(conn: lb.Connection, tieu_de: str, cau_lenh: str, tham_so: dict) -> None:
    """Chạy một truy vấn và in tên cột cùng các dòng kết quả."""
    ket_qua = conn.execute(cau_lenh, parameters=tham_so)
    ten_cot = ket_qua.get_column_names()
    print(tieu_de)
    print(" | ".join(ten_cot))
    print("-" * (len(" | ".join(ten_cot))))
    for dong in ket_qua:
        print(" | ".join(str(gia_tri) for gia_tri in dong))
    print()


def main() -> None:
    """Mở database đã tạo và chạy lần lượt các truy vấn TV4."""
    if not DUONG_DAN_DB.exists():
        raise SystemExit(
            "Chưa có campus_graph.lbdb. Hãy chạy 01_setup_db.py trước."
        )

    db = lb.Database(str(DUONG_DAN_DB), read_only=True)
    conn = lb.Connection(db)
    try:
        for tieu_de, cau_lenh, tham_so in TRUY_VAN:
            in_ket_qua(conn, tieu_de, cau_lenh, tham_so)
    finally:
        conn.close()
        db.close()


if __name__ == "__main__":
    main()
