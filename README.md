# Đồ án cuối kỳ môn Lý thuyết đồ thị – LadybugDB

Kho lưu trữ mã nguồn thực hành và hình ảnh minh họa cho đồ án cuối kỳ môn **Lý thuyết đồ thị**, tìm hiểu và triển khai hệ quản trị cơ sở dữ liệu đồ thị nhúng **LadybugDB** bằng ngôn ngữ **Python** và ngôn ngữ truy vấn **Cypher**.

---

## 1. Giới thiệu bài toán minh họa: Campus Graph

Để thể hiện rõ cả khả năng truy vấn thuộc tính (tương đương `SELECT ... FROM ... WHERE` trong SQL) lẫn các thuật toán tìm đường đi ngắn nhất trong Lý thuyết đồ thị, đồ án xây dựng mô hình **Campus Graph** (bản đồ khuôn viên trường kết hợp dữ liệu học tập của sinh viên) trong cùng một cơ sở dữ liệu đồ thị thuộc tính có lược đồ chặt chẽ (*Structured Property Graph*):

| Thành phần | Tên bảng | Thuộc tính chính | Mô tả |
| :--- | :--- | :--- | :--- |
| `NODE TABLE` | `SinhVien` | `ma_sv` (PK), `ten`, `lop` | 6 sinh viên |
| `NODE TABLE` | `MonHoc` | `ma_mon` (PK), `ten_mon`, `tin_chi` | 4 môn học |
| `NODE TABLE` | `ToaNha` | `ma` (PK), `ten` | 8 tòa nhà (`KTX`, `A`, `B`, `C`, `TV`, `CT`, `TN`, `TD`) |
| `REL TABLE` | `HOC` (`SinhVien -> MonHoc`) | `diem` | Điểm thi của sinh viên theo từng môn |
| `REL TABLE` | `HOC_TAI` (`MonHoc -> ToaNha`) | `phong` | Địa điểm (tòa nhà, phòng học) của từng môn |
| `REL TABLE` | `LOI_DI` (`ToaNha -> ToaNha`) | `met` | 13 lối đi giữa các tòa nhà với trọng số là độ dài (mét) |

---

## 2. Các truy vấn minh họa trong đồ án

1. **Tìm sinh viên có điểm thi cao nhất** môn *Lý thuyết đồ thị* (`MATCH ... ORDER BY ... DESC LIMIT 1`).
2. **Tính điểm trung bình và xếp hạng** sinh viên (tổng hợp `AVG`, `ORDER BY`).
3. **Lọc danh sách sinh viên trượt môn** (`WHERE diem < 5.0`).
4. **Đường đi ngắn nhất không trọng số (`SHORTEST` – thuật toán BFS):** từ `KTX` đến tòa `C` qua ít tòa nhà nhất (`KTX -> A -> C`, 2 cạnh, tổng 850 m).
5. **Đường đi ngắn nhất có trọng số (`WSHORTEST` – thuật toán Dijkstra):** từ `KTX` đến tòa `C` có tổng độ dài nhỏ nhất (`KTX -> CT -> TV -> C`, 3 cạnh, tổng 450 m).
6. **Truy vấn tổng hợp đa bước:** tìm lộ trình ngắn nhất từ `KTX` đến tòa nhà học môn *Lý thuyết đồ thị* của sinh viên Nguyễn Văn An (`KTX -> CT -> B`, tổng 370 m).

---

## 3. Cấu trúc thư mục

```text
.
├── README.md                  # Tài liệu giới thiệu và hướng dẫn chạy dự án
├── requirements.txt           # Danh sách thư viện Python cần cài đặt (ladybug)
├── .gitignore                 # Loại trừ môi trường ảo và tệp cơ sở dữ liệu tạm
├── images/                    # Sơ đồ đồ thị Campus Graph và ảnh kết quả thực thi
└── src/                       # Mã nguồn Python thực hành (cấu trúc chuẩn của nhóm)
    ├── 01_setup_db.py         # Khởi tạo lược đồ (NODE/REL TABLE) và nạp dữ liệu Campus Graph
    ├── 02_basic_queries.py    # Thực thi các truy vấn lọc, tổng hợp, xếp hạng (Câu 1–3)
    └── 03_shortest_path.py    # Thực thi các truy vấn đường đi ngắn nhất (Câu 4–6)
```

---

## 4. Hướng dẫn cài đặt và chạy chương trình

**Yêu cầu:** Python 3.9 trở lên.

```bash
# Bước 1: Tạo và kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows (Command Prompt / PowerShell)

# Bước 2: Cài đặt thư viện LadybugDB
pip install -r requirements.txt

# Bước 3: Chạy lần lượt các kịch bản thực hành (sau khi hoàn thiện mã nguồn trong src/)
python src/01_setup_db.py
python src/02_basic_queries.py
python src/03_shortest_path.py
```

---

## 5. Lưu ý quản lý mã nguồn

- Mọi tệp cơ sở dữ liệu sinh ra trong quá trình chạy thử (`db/`, `*.lbug`) và môi trường ảo (`.venv/`) đều được loại trừ trong `.gitignore` để giữ kho lưu trữ sạch sẽ.
- Phân công cụ thể các thành viên và lịch sử đóng góp được quản lý qua nhánh và Pull Request trên kho lưu trữ này (nhánh `main` lưu trữ phiên bản chính thức).
