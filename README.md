# Đồ án cuối kỳ Lý thuyết đồ thị – LadybugDB

Kho lưu trữ mã nguồn thực hành và dữ liệu minh họa cho đồ án môn **Lý thuyết đồ thị** với đề tài **LadybugDB** (nhóm 5 thành viên).

- **Bài toán minh họa:** Hệ thống **Campus Graph** (Bản đồ khuôn viên trường gồm 8 tòa nhà, 13 lối đi có trọng số mét + 6 sinh viên, 4 môn học và điểm thi).
- **Mục tiêu demo:** Đối chiếu truy vấn lọc/xếp hạng kiểu SQL (`SELECT-FROM-WHERE`) bằng Cypher và so sánh trực quan đường đi ngắn nhất không trọng số (`SHORTEST` – BFS) với có trọng số (`WSHORTEST` – Dijkstra).

## 1. Cấu trúc thư mục dự kiến

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── images/                  # Sơ đồ đồ thị mẫu và ảnh chụp kết quả chạy
└── src/                     # Mã nguồn Python thực hành
    ├── 01_setup_db.py       # (TV4) Khởi tạo NODE TABLE, REL TABLE và nạp dữ liệu mẫu
    ├── 02_basic_queries.py  # (TV4) Các truy vấn lọc/xếp hạng (tương đương SELECT-FROM-WHERE)
    └── 03_shortest_path.py  # (TV5) Các truy vấn đường đi ngắn nhất (SHORTEST, WSHORTEST)
```

## 2. Hướng dẫn cài đặt môi trường

```bash
# Tạo và kích hoạt môi trường ảo (khuyên dùng)
python3 -m venv .venv
source .venv/bin/activate   # Trên Windows: .venv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt
```

## 3. Quy ước làm việc trên GitHub (dành cho nhóm)

- **TV1 (Leader):** Quản lý nhánh `main`, kiểm tra và duyệt Pull Request (PR) từ các thành viên.
- **TV4:** Làm việc trên nhánh `feat/setup-and-basic`, phụ trách `src/01_setup_db.py`, `src/02_basic_queries.py` và hình sơ đồ đồ thị mẫu trong `images/`.
- **TV5:** Sau khi TV4 merge phần khởi tạo DB vào `main`, tạo nhánh `feat/shortest-path`, phụ trách `src/03_shortest_path.py` và ảnh kết quả chạy trong `images/`.
- **Lưu ý:** Không push thư mục `.venv/` hoặc file database sinh ra khi chạy thử (`db/`, `*.lbug`). Báo cáo Word và Slide làm chung trên Google Docs / Google Slides, không đẩy lên GitHub.
