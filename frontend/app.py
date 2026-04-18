import os
import base64
import requests
import datetime
import streamlit as st
import pandas as pd

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Quản lý chi tiêu", layout="centered")

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

def render_background(image_name):
    pic_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pic", image_name))
    if os.path.exists(pic_path):
        with open(pic_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
        st.markdown(css, unsafe_allow_html=True)

import json

def save_session():
    try:
        with open(".session_cache.json", "w", encoding="utf-8") as f:
            json.dump({
                "token": st.session_state.token,
                "email": st.session_state.email
            }, f)
    except Exception:
        pass

def load_session():
    if "token" not in st.session_state:
        st.session_state.token = None
        st.session_state.email = None
        try:
            if os.path.exists(".session_cache.json"):
                with open(".session_cache.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    st.session_state.token = data.get("token")
                    st.session_state.email = data.get("email")
        except Exception:
            pass

load_session()

def format_vnd(amount_str):
    clean_str = ''.join(c for c in str(amount_str) if c.isdigit())
    if not clean_str:
        return 0.0
    return float(clean_str)

def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass

def handle_google_login_callback():
    if st.session_state.token:
        return

    params = st.query_params
    raw_token = params.get("id_token")

    if not raw_token:
        return

    id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

    try:
        res = requests.post(f"{API_URL}/auth/google", json={"id_token": id_token})
        if res.status_code == 200:
            user_data = res.json()
            st.session_state.token = user_data["idToken"]
            st.session_state.email = user_data["email"] or "Người dùng Google"
            save_session()
            clear_google_query_params()
            st.success("Đăng nhập Google thành công!")
            st.rerun()
        else:
            st.error(f"Đăng nhập Google thất bại: {res.json().get('detail')}")
            clear_google_query_params()
    except Exception as e:
        st.error(f"Lỗi xử lý Google login: {e}")
        clear_google_query_params()

handle_google_login_callback()

st.markdown('<div style="text-align: center;"><div class="main-header">QUẢN LÝ CHI TIÊU</div></div>', unsafe_allow_html=True)

if not st.session_state.token:
    render_background("t12025.png")
    st.markdown('<div class="sub-header">Đăng nhập / Đăng ký hệ thống</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        /* Riêng ngoài Tab Đăng nhập, text label giữ màu Trắng tinh */
        label[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] span {
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký mới"])
    
    with tab1:
        with st.container(border=True):
            email = st.text_input("Tài khoản Email", key="login_email")
            password = st.text_input("Mật khẩu", type="password", key="login_pass")
            if st.button("Đăng nhập", use_container_width=True, type="primary"):
                res = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json().get("idToken")
                    st.session_state.email = email
                    save_session()
                    st.rerun()
                else:
                    st.error(f"Lỗi: {res.json().get('detail')}")

            try:
                google_login_url = dict(st.secrets.get("google-login", {})).get("google-url")
                if google_login_url:
                    st.markdown(
                    f'''
                    <a href="{google_login_url}" target="_self" style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                        padding: 0.5rem 1rem;
                        background-color: white;
                        color: #444;
                        text-decoration: none;
                        border-radius: 0.5rem;
                        border: 1px solid #ccc;
                        font-weight: 600;
                        margin-top: 15px;
                    ">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" width="18" height="18" alt="Google">
                        Đăng nhập với Google
                    </a>
                    ''',
                    unsafe_allow_html=True,
                )
                else:
                    st.info("Chưa cấu hình URL Google Login trong secrets.toml")
            except Exception:
                st.info("Chưa cấu hình google-login")

    with tab2:
         with st.container(border=True):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Mật khẩu", type="password", key="reg_pass")
            if st.button("Tạo tài khoản", use_container_width=True):
                res = requests.post(f"{API_URL}/auth/signup", json={"email": reg_email, "password": reg_password})
                if res.status_code == 200:
                    st.success("Tạo tài khoản thành công! Hãy chuyển sang trang Đăng nhập.")
                else:
                    st.error(f"Lỗi: {res.json().get('detail')}")
                    
else:
    render_background("faker.png")
    
    st.markdown("""
        <style>
        /* Riêng Form nhập liệu nền Faker sáng, Label chữ bắt buộc Phải Đen */
        label[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] span {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown(f"### Xin chào,\n**{st.session_state.email}**")
    if st.sidebar.button("Đăng xuất", use_container_width=True):
        st.session_state.token = None
        st.session_state.email = None
        save_session()
        st.rerun()

    # Main Area
    st.markdown('<div class="sub-header">Nhập khoản chi mới</div>', unsafe_allow_html=True)
    with st.form("expense", border=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Tên khoản chi", placeholder="Ví dụ: Ăn trưa, Đổ xăng...")
            date_obj = st.date_input("Ngày chi", datetime.date.today(), format="DD/MM/YYYY")
        with col2:
            amount_str = st.text_input("Số tiền", placeholder="VD: 1.000.000")
            category = st.selectbox("Phân loại", ["Ăn uống", "Đi lại", "Mua sắm", "Hóa đơn", "Khác"])
            
        submit = st.form_submit_button("Lưu Dữ Liệu", use_container_width=True, type="primary")
        
        if submit:
            amount_val = format_vnd(amount_str)
            if amount_val <= 0 or not name.strip():
                st.warning("Vui lòng nhập tên khoản chi và số tiền hợp lệ!")
            else:
                payload = {"name": name, "amount": amount_val, "date": str(date_obj), "category": category}
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                res = requests.post(f"{API_URL}/expenses", json=payload, headers=headers)
                
                if res.status_code == 200:
                    formatted_val = f"{amount_val:,.0f} VNĐ".replace(",", ".")
                    st.success(f"Đã lưu thành công: **{name}** với số tiền **{formatted_val}**")
                elif res.status_code == 401:
                    st.error("Phiên đăng nhập đã hết hạn. Vui lòng đăng xuất và đăng nhập lại!")
                else:
                    st.error(f"Lỗi máy chủ: {res.text}")

    st.markdown('<div class="sub-header">Lịch sử chi tiêu</div>', unsafe_allow_html=True)
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    res = requests.get(f"{API_URL}/expenses", headers=headers)
    
    if res.status_code == 200:
        data = res.json()
        if len(data) > 0:
            df = pd.DataFrame(data)
            
            # Xu ly ngay thang de thong ke
            df["date_parse"] = pd.to_datetime(df["date"])
            df["Tháng"] = df["date_parse"].dt.strftime("%m/%Y")
            df["Ngày"] = df["date_parse"].dt.strftime("%d/%m/%Y")
            df["Khoản chi"] = df["name"]
            df["Danh mục"] = df.get("category", "Khác")
            df["Số tiền"] = df["amount"].apply(lambda x: f"{x:,.0f} VNĐ".replace(",", "."))
            
            # Tinh toan Thong ke
            total = sum(d["amount"] for d in data)
            monthly_summary = df.groupby("Tháng")["amount"].agg(["sum", "count"]).reset_index()
            monthly_summary.sort_values(by="Tháng", ascending=False, inplace=True)
            num_months = len(monthly_summary)
            avg_per_month = total / num_months if num_months > 0 else 0
            
            # Hien thi giao dien the Metric
            st.markdown("### Phân tích tổng quan")
            col1, col2 = st.columns(2)
            
            def render_custom_metric(label, value):
                return f"""
                <div class="custom-metric-box">
                    <p style="font-size: 1.2rem; margin: 0; padding-bottom: 5px;">{label}</p>
                    <p style="font-size: 2.2rem; margin: 0;">{value}</p>
                </div>
                """
                
            with col1:
                st.markdown(render_custom_metric("Tổng chi tiêu", f"{total:,.0f} VNĐ".replace(",", ".")), unsafe_allow_html=True)
            with col2:
                st.markdown(render_custom_metric("Trung bình mỗi tháng", f"{avg_per_month:,.0f} VNĐ".replace(",", ".")), unsafe_allow_html=True)
            
            # Hien thi Bang tong theo thang
            st.markdown("### Thống kê từng tháng")
            monthly_summary.rename(columns={"sum": "Tổng tiền chi", "count": "Số khoản"}, inplace=True)
            monthly_summary["Tổng tiền chi"] = monthly_summary["Tổng tiền chi"].apply(lambda x: f"{x:,.0f} VNĐ".replace(",", "."))
            st.dataframe(monthly_summary[["Tháng", "Số khoản", "Tổng tiền chi"]], use_container_width=True, hide_index=True)
            
            # Hien thi Toan bo lich su
            st.markdown("### Nhật ký giao dịch chi tiết")
            st.dataframe(df[["Ngày", "Khoản chi", "Danh mục", "Số tiền"]], use_container_width=True, hide_index=True)
            
            # Giao dien Xoa
            with st.expander(" Xóa giao dịch"):
                st.write("Chọn giao dịch bạn muốn xóa:")
                sorted_data = sorted(data, key=lambda x: x["date"], reverse=True)
                
                # Format ngay Date thanh dd/mm/yyyy trong danh sach Xoa
                def format_date_ddmmyyyy(date_str):
                    parts = date_str.split('-')
                    if len(parts) == 3:
                        return f"{parts[2]}/{parts[1]}/{parts[0]}"
                    return date_str
                    
                options = {f"[{format_date_ddmmyyyy(d['date'])}] {d['name']} - {d['amount']:,.0f} VNĐ": d["id"] for d in sorted_data}
                selected_label = st.selectbox("Danh sách giao dịch", list(options.keys()))
                
                if st.button("Xóa khoản chi này", type="primary"):
                    expense_id = options[selected_label]
                    del_res = requests.delete(f"{API_URL}/expenses/{expense_id}", headers=headers)
                    if del_res.status_code == 200:
                        st.success("Đã xóa thành công!")
                        st.rerun()
                    else:
                        st.error("Lỗi: Không thể xóa giao dịch này.")
        else:
            st.info("Chưa có giao dịch.")
    elif res.status_code == 401:
        st.error("Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.")
        st.session_state.token = None
        st.session_state.email = None
        save_session()
        st.rerun()
