# Ứng dụng Quản lý Chi Tiêu

Một ứng dụng theo dõi chi tiêu cá nhân sử dụng **FastAPI** cho Backend và **Streamlit** cho Frontend. Tích hợp Firebase Authentication và Firestore.

## 1. Hướng cài đặt môi trường
Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
# Trên Windows
venv\Scripts\activate
# Trên MacOS/Linux
source venv/bin/activate
```

Cài đặt tất cả thư viện cần thiết cho cả Frontend và Backend:
```bash
pip install -r requirements.txt
```

## 2. Truy cập hệ thống Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
API sẽ hoạt động tại `http://localhost:8000`.

## 3. Chạy giao diện Frontend
Mở một terminal mới, kích hoạt lại môi trường ảo:
```bash
streamlit run frontend/app.py
```
Giao diện sẽ khởi chạy tại `http://localhost:8501`.

## 4. Video Demo
[Chèn đường dẫn Video Demo tại đây]
