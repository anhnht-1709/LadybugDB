"""Khởi tạo cơ sở dữ liệu Campus Graph cho đồ án Lý thuyết đồ thị."""
import argparse
import shutil
from pathlib import Path

import ladybug as lb


THU_MUC = Path(__file__).resolve().parent
DUONG_DAN_DB = THU_MUC / "campus_graph.lbdb"
DUONG_DAN_WAL = Path(str(DUONG_DAN_DB) + ".wal")

TOA_NHA = [
    ("KTX", "Ký túc xá"),
    ("A", "Hành chính"),
    ("B", "CNTT"),
    ("C", "Giảng đường trung tâm"),
    ("TV", "Thư viện"),
    ("CT", "Căng tin"),
    ("TN", "Khu thí nghiệm"),
    ("TD", "Nhà thi đấu"),
]

MON_HOC = [
    ("LTDT", "Lý thuyết đồ thị", 3, "B", "B201"),
    ("CSDL", "Cơ sở dữ liệu", 3, "C", "C302"),
    ("CTDL", "Cấu trúc dữ liệu & Giải thuật", 4, "TN", "TN105"),
    ("MMT", "Mạng máy tính", 3, "A", "A102"),
]

SINH_VIEN = [
    ("SV01", "Nguyễn Văn An", "CNTT01"),
    ("SV02", "Trần Thị Bình", "CNTT01"),
    ("SV03", "Lê Hoàng Cường", "CNTT02"),
    ("SV04", "Phạm Minh Dung", "CNTT02"),
    ("SV05", "Hoàng Quốc Em", "CNTT01"),
    ("SV06", "Vũ Thảo Phương", "CNTT02"),
]

DIEM_THI = {
    "SV01": {"LTDT": 8.5, "CSDL": 7.5, "CTDL": 8.0},
    "SV02": {"LTDT": 9.5, "CSDL": 9.0, "MMT": 8.5},
    "SV03": {"LTDT": 4.0, "CSDL": 6.5, "CTDL": 5.5},
    "SV04": {"LTDT": 7.0, "CTDL": 9.0, "MMT": 8.0},
    "SV05": {"CSDL": 4.5, "CTDL": 4.0, "MMT": 6.0},
    "SV06": {"LTDT": 8.0, "CSDL": 8.5, "MMT": 9.0},
}

# Mỗi lối đi chỉ lưu một quan hệ; truy vấn sẽ xét quan hệ theo cả hai chiều.
LOI_DI = [
    ("KTX", "A", 450),
    ("KTX", "CT", 150),
    ("KTX", "TD", 200),
    ("A", "C", 400),
    ("A", "TV", 180),
    ("CT", "TV", 120),
    ("CT", "B", 220),
    ("TD", "B", 250),
    ("TV", "C", 180),
    ("TV", "TN", 260),
    ("B", "C", 160),
    ("B", "TN", 140),
    ("TN", "C", 150),
]


def xoa_du_lieu_cu(duong_dan: Path) -> None:
    """Xóa đúng database Campus Graph cũ và tệp WAL của nó."""
    if duong_dan.is_dir():
        shutil.rmtree(duong_dan)
    elif duong_dan.exists():
        duong_dan.unlink()


def tao_luoc_do(conn: lb.Connection) -> None:
    """Tạo các bảng nút và bảng quan hệ."""
    conn.execute(
        "CREATE NODE TABLE SinhVien(" 
        "ma_sv STRING PRIMARY KEY, ten STRING, lop STRING)"
    )
    conn.execute(
        "CREATE NODE TABLE MonHoc(" 
        "ma_mon STRING PRIMARY KEY, ten_mon STRING, tin_chi INT64)"
    )
    conn.execute(
        "CREATE NODE TABLE ToaNha(ma STRING PRIMARY KEY, ten STRING)"
    )
    conn.execute(
        "CREATE REL TABLE HOC(FROM SinhVien TO MonHoc, diem DOUBLE)"
    )
    conn.execute(
        "CREATE REL TABLE HOC_TAI(FROM MonHoc TO ToaNha, phong STRING)"
    )
    conn.execute(
        "CREATE REL TABLE LOI_DI(FROM ToaNha TO ToaNha, met INT64)"
    )


def nap_du_lieu(conn: lb.Connection) -> None:
    """Nạp nút và quan hệ Campus Graph từ các danh sách dữ liệu."""
    for ma, ten in TOA_NHA:
        conn.execute(
            "CREATE (:ToaNha {ma: $ma, ten: $ten})",
            parameters={"ma": ma, "ten": ten},
        )

    for ma_mon, ten_mon, tin_chi, ma_toa, phong in MON_HOC:
        conn.execute(
            "CREATE (:MonHoc {ma_mon: $ma_mon, ten_mon: $ten_mon, "
            "tin_chi: $tin_chi})",
            parameters={
                "ma_mon": ma_mon,
                "ten_mon": ten_mon,
                "tin_chi": tin_chi,
            },
        )
        conn.execute(
            "MATCH (m:MonHoc {ma_mon: $ma_mon}), "
            "(t:ToaNha {ma: $ma_toa}) "
            "CREATE (m)-[:HOC_TAI {phong: $phong}]->(t)",
            parameters={"ma_mon": ma_mon, "ma_toa": ma_toa, "phong": phong},
        )

    for ma_sv, ten, lop in SINH_VIEN:
        conn.execute(
            "CREATE (:SinhVien {ma_sv: $ma_sv, ten: $ten, lop: $lop})",
            parameters={"ma_sv": ma_sv, "ten": ten, "lop": lop},
        )

    for ma_sv, cac_mon in DIEM_THI.items():
        for ma_mon, diem in cac_mon.items():
            conn.execute(
                "MATCH (s:SinhVien {ma_sv: $ma_sv}), "
                "(m:MonHoc {ma_mon: $ma_mon}) "
                "CREATE (s)-[:HOC {diem: $diem}]->(m)",
                parameters={"ma_sv": ma_sv, "ma_mon": ma_mon, "diem": diem},
            )

    for ma_dau, ma_cuoi, so_met in LOI_DI:
        conn.execute(
            "MATCH (a:ToaNha {ma: $ma_dau}), (b:ToaNha {ma: $ma_cuoi}) "
            "CREATE (a)-[:LOI_DI {met: $so_met}]->(b)",
            parameters={"ma_dau": ma_dau, "ma_cuoi": ma_cuoi, "so_met": so_met},
        )


def main() -> None:
    """Tạo mới database; chỉ xóa database cũ khi người dùng truyền --reset."""
    bo_doc = argparse.ArgumentParser(
        description="Khởi tạo database Campus Graph dùng cho các truy vấn đồ thị."
    )
    bo_doc.add_argument(
        "--reset",
        action="store_true",
        help="xóa database Campus Graph cũ trước khi tạo lại",
    )
    tuy_chon = bo_doc.parse_args()

    if DUONG_DAN_DB.exists() or DUONG_DAN_WAL.exists():
        if not tuy_chon.reset:
            raise SystemExit(
                f"Database đã tồn tại ở {DUONG_DAN_DB}. "
                "Chạy lại với --reset nếu muốn xóa và tạo mới."
            )
        xoa_du_lieu_cu(DUONG_DAN_DB)
        xoa_du_lieu_cu(DUONG_DAN_WAL)
        print("Đã xóa database Campus Graph cũ.")

    db = lb.Database(str(DUONG_DAN_DB))
    conn = lb.Connection(db)
    try:
        tao_luoc_do(conn)
        nap_du_lieu(conn)
        print(f"Đã tạo database Campus Graph tại: {DUONG_DAN_DB}")
        print("Đã nạp 8 tòa nhà, 4 môn học, 6 sinh viên và 13 lối đi.")
    finally:
        conn.close()
        db.close()


if __name__ == "__main__":
    main()
