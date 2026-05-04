# Ứng dụng Quản lý Chi Tiêu

Ứng dụng theo dõi chi tiêu cá nhân được phát triển bằng **FastAPI** (Backend) và **Streamlit** (Frontend), kết hợp hệ thống lưu trữ dữ liệu đám mây **Firebase (Auth & Firestore)**.

---
## Yêu cầu

* Python 3.10
* Streamlit
* Các thư viện trong file `requirements.txt`

## Cài đặt environment

Đảm bảo máy tính của bạn đã cài đặt Python 3.10 trở lên.

**Bước 1: Tạo và kích hoạt môi trường ảo (Virtual Environment)**
Tại thư mục gốc của dự án, mở Terminal và chạy lệnh:
```bash
python -m venv venv

# Trên Windows
venv\Scripts\activate

# Trên MacOS/Linux
source venv/bin/activate
```

**Bước 2: Cài đặt các thư viện**
Sau khi môi trường ảo được kích hoạt thành công, chạy lệnh sau để tải toàn bộ thư viện cần thiết cho dự án:
```bash
pip install -r requirements.txt
```

---

## Chạy backend

Backend chịu trách nhiệm xác thực người dùng và xử lý tương tác với Firestore Database.

1. Đảm bảo môi trường ảo `venv` đang được kích hoạt trên Terminal.
2. Di chuyển vào thư mục `backend` và khởi chạy server API:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
Server Backend sẽ hoạt động ổn định tại: `http://localhost:8000` (Có thể xem API Docs tại `http://localhost:8000/docs`).

---

## Chạy frontend

Frontend được xây dựng bằng Streamlit và là phần giao diện chính mà người dùng sẽ thao tác.

1. Mở một Terminal mới (hoặc tách nhánh Terminal hiện tại).
2. Đảm bảo Terminal mới **đang ở thư mục gốc** của dự án (`tdtt_lab2`) và **đã kích hoạt lại môi trường ảo**:

```bash
# Trên Windows
venv\Scripts\activate
```

3. Khởi chạy ứng dụng:

```bash
streamlit run frontend/app.py
```

Giao diện sẽ tự động bật lên trên trình duyệt qua địa chỉ: `http://localhost:8501`.

---

## Đường dẫn đến video demo

Mọi phân hệ chức năng từ Đăng nhập, Nhập liệu, Thống kê cho đến Quản lý tài khoản cục bộ đều được vận hành mượt mà trong giao diện Dark Mode xuyên suốt dự án. Xem chi tiết hoạt động qua Video sau: `https://youtu.be/-Rqi05uVNMg`
