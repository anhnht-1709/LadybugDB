"""Initialize the Campus Graph database for the Graph Theory assignment."""
from pathlib import Path
import ladybug as lb

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "campus_graph.lbdb"
BUILDINGS = [("KTX", "Ký túc xá"), ("A", "Hành chính"), ("B", "CNTT"), ("C", "Giảng đường trung tâm"), ("TV", "Thư viện"), ("CT", "Căng tin"), ("TN", "Khu thí nghiệm"), ("TD", "Nhà thi đấu")]
COURSES = [("LTDT", "Lý thuyết đồ thị", 3, "B", "B201"), ("CSDL", "Cơ sở dữ liệu", 3, "C", "C302"), ("CTDL", "Cấu trúc dữ liệu & Giải thuật", 4, "TN", "TN105"), ("MMT", "Mạng máy tính", 3, "A", "A102")]
STUDENTS = [("SV01", "Nguyễn Văn An", "CNTT01"), ("SV02", "Trần Thị Bình", "CNTT01"), ("SV03", "Lê Hoàng Cường", "CNTT02"), ("SV04", "Phạm Minh Dung", "CNTT02"), ("SV05", "Hoàng Quốc Em", "CNTT01"), ("SV06", "Vũ Thảo Phương", "CNTT02")]
GRADES = {"SV01": {"LTDT": 8.5, "CSDL": 7.5, "CTDL": 8.0}, "SV02": {"LTDT": 9.5, "CSDL": 9.0, "MMT": 8.5}, "SV03": {"LTDT": 4.0, "CSDL": 6.5, "CTDL": 5.5}, "SV04": {"LTDT": 7.0, "CTDL": 9.0, "MMT": 8.0}, "SV05": {"CSDL": 4.5, "CTDL": 4.0, "MMT": 6.0}, "SV06": {"LTDT": 8.0, "CSDL": 8.5, "MMT": 9.0}}
# The brief says these walkways can be used in both directions.
WALKS = [("KTX", "A", 450), ("KTX", "CT", 150), ("KTX", "TD", 200), ("A", "C", 400), ("A", "TV", 180), ("CT", "TV", 120), ("CT", "B", 220), ("TD", "B", 250), ("TV", "C", 180), ("TV", "TN", 260), ("B", "C", 160), ("B", "TN", 140), ("TN", "C", 150)]

def main():
    if DB_PATH.exists():
        raise SystemExit(f"Database already exists: {DB_PATH}. Move it aside before rebuilding.")
    db = lb.Database(str(DB_PATH))
    conn = lb.Connection(db)
    try:
        conn.execute("CREATE NODE TABLE SinhVien(ma_sv STRING PRIMARY KEY, ten STRING, lop STRING)")
        conn.execute("CREATE NODE TABLE MonHoc(ma_mon STRING PRIMARY KEY, ten_mon STRING, tin_chi INT64)")
        conn.execute("CREATE NODE TABLE ToaNha(ma STRING PRIMARY KEY, ten STRING)")
        conn.execute("CREATE REL TABLE HOC(FROM SinhVien TO MonHoc, diem DOUBLE)")
        conn.execute("CREATE REL TABLE HOC_TAI(FROM MonHoc TO ToaNha, phong STRING)")
        conn.execute("CREATE REL TABLE LOI_DI(FROM ToaNha TO ToaNha, met INT64)")
        for code, name in BUILDINGS:
            conn.execute(f"CREATE (:ToaNha {{ma: '{code}', ten: '{name}'}})")
        for code, name, credits, building, room in COURSES:
            conn.execute(f"CREATE (:MonHoc {{ma_mon: '{code}', ten_mon: '{name}', tin_chi: {credits}}})")
            conn.execute(f"MATCH (m:MonHoc {{ma_mon: '{code}'}}), (t:ToaNha {{ma: '{building}'}}) CREATE (m)-[:HOC_TAI {{phong: '{room}'}}]->(t)")
        for sid, name, cohort in STUDENTS:
            conn.execute(f"CREATE (:SinhVien {{ma_sv: '{sid}', ten: '{name}', lop: '{cohort}'}})")
        for sid, grades in GRADES.items():
            for course, score in grades.items():
                conn.execute(f"MATCH (s:SinhVien {{ma_sv: '{sid}'}}), (m:MonHoc {{ma_mon: '{course}'}}) CREATE (s)-[:HOC {{diem: {score}}}]->(m)")
        for left, right, metres in WALKS:
            for source, target in ((left, right), (right, left)):
                conn.execute(f"MATCH (a:ToaNha {{ma: '{source}'}}), (b:ToaNha {{ma: '{target}'}}) CREATE (a)-[:LOI_DI {{met: {metres}}}]->(b)")
        print(f"Campus Graph initialized: {DB_PATH}")
    finally:
        conn.close()
        db.close()

if __name__ == "__main__":
    main()
