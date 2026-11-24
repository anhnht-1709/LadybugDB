"""Chạy ba truy vấn đường đi ngắn nhất được phân công cho TV5 (Câu 4-6)."""
from pathlib import Path

import ladybug as lb


DUONG_DAN_DB = Path(__file__).resolve().parent / "campus_graph.lbdb"

# Ghi chú chung cho cả ba câu:
# - LOI_DI chỉ lưu một chiều (xem 01_setup_db.py), nên mẫu cạnh được viết
#   KHÔNG có mũi tên: -[:LOI_DI* ...]-  để đi được cả hai chiều.
# - Tổng số mét lấy từ danh sách properties(rels(p), 'met') rồi cộng bằng
#   list_sum, không dùng cost(p) vì hàm này làm ladybug 0.22.3 bị crash.
# - Campus có 8 tòa nhà nên một đường đi đơn dài tối đa 7 cạnh -> cận 1..7.

TRUY_VAN = [
    (
        "Câu 4 - Đường từ KTX đến C qua ít tòa nhà nhất (SHORTEST / BFS)",
        """MATCH p = (dau:ToaNha)-[:LOI_DI* SHORTEST 1..7]-(cuoi:ToaNha)
        WHERE dau.ma = $diem_dau AND cuoi.ma = $diem_cuoi
        RETURN properties(nodes(p), 'ma') AS lo_trinh,
               length(p) AS so_canh,
               properties(rels(p), 'met') AS met_tung_canh,
               list_sum(properties(rels(p), 'met')) AS tong_met""",
        {"diem_dau": "KTX", "diem_cuoi": "C"},
    ),
    (
        "Câu 5 - Đường từ KTX đến C có tổng số mét nhỏ nhất (WSHORTEST / Dijkstra)",
        """MATCH p = (dau:ToaNha)-[:LOI_DI* WSHORTEST(met)]-(cuoi:ToaNha)
        WHERE dau.ma = $diem_dau AND cuoi.ma = $diem_cuoi
        RETURN properties(nodes(p), 'ma') AS lo_trinh,
               length(p) AS so_canh,
               properties(rels(p), 'met') AS met_tung_canh,
               list_sum(properties(rels(p), 'met')) AS tong_met""",
        {"diem_dau": "KTX", "diem_cuoi": "C"},
    ),
    (
        "Câu 6 - Nguyễn Văn An đi từ KTX đến lớp Lý thuyết đồ thị",
        # MATCH thứ nhất: SinhVien -HOC-> MonHoc -HOC_TAI-> ToaNha để tìm
        # tòa nhà (và phòng) mà An học LTDT.
        # MATCH thứ hai: dùng chính tòa nhà đó làm đích cho WSHORTEST.
        """MATCH (s:SinhVien)-[:HOC]->(m:MonHoc)-[ht:HOC_TAI]->(dich:ToaNha)
        WHERE s.ten = $ten_sv AND m.ma_mon = $ma_mon
        MATCH p = (dau:ToaNha)-[:LOI_DI* WSHORTEST(met)]-(dich)
        WHERE dau.ma = $diem_dau
        RETURN s.ten AS ten_sinh_vien, m.ten_mon AS ten_mon_hoc,
               dich.ma AS toa_nha, ht.phong AS phong,
               properties(nodes(p), 'ma') AS lo_trinh,
               properties(rels(p), 'met') AS met_tung_canh,
               list_sum(properties(rels(p), 'met')) AS tong_met""",
        {"ten_sv": "Nguyễn Văn An", "ma_mon": "LTDT", "diem_dau": "KTX"},
    ),
]


def dinh_dang(ten_cot: str, gia_tri) -> str:
    """Đổi danh sách tòa nhà và danh sách số mét thành chuỗi dễ đọc."""
    if ten_cot == "lo_trinh":
        return " -> ".join(gia_tri)
    if ten_cot == "met_tung_canh":
        return " + ".join(str(so_met) for so_met in gia_tri)
    return str(gia_tri)


def in_ket_qua(conn: lb.Connection, tieu_de: str, cau_lenh: str, tham_so: dict) -> None:
    """Chạy một truy vấn và in tên cột cùng các dòng kết quả."""
    ket_qua = conn.execute(cau_lenh, parameters=tham_so)
    ten_cot = ket_qua.get_column_names()
    print(tieu_de)
    print(" | ".join(ten_cot))
    print("-" * (len(" | ".join(ten_cot))))
    for dong in ket_qua:
        print(" | ".join(dinh_dang(cot, gia_tri) for cot, gia_tri in zip(ten_cot, dong)))
    print()


def main() -> None:
    """Mở database đã tạo và chạy lần lượt các truy vấn TV5."""
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
