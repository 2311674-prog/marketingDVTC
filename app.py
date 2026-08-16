import streamlit as st
import pandas as pd

# Cấu hình giao diện trang
st.set_page_config(page_title="Quản lý Thông tin Khách hàng", layout="centered")

# Khởi tạo session state để lưu trữ dữ liệu tạm thời
if "df_khach_hang" not in st.empty():
    if "df_khach_hang" not in st.session_state:
        st.session_state.df_khach_hang = pd.DataFrame(
            columns=["Số điện thoại", "Tên khách hàng", "Khu vực", "Ghi chú"]
        )

st.title("📋 Nhập Thông Tin Khách Hàng")

# Form nhập thông tin
with st.form(key="form_khach_hang", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        sdt = st.text_input("Số điện thoại *", placeholder="VD: 0912345678")
        ten = st.text_input("Tên khách hàng *", placeholder="VD: Nguyễn Văn A")

    with col2:
        khu_vuc = st.selectbox(
            "Khu vực",
            ["Miền Bắc", "Miền Trung", "Miền Nam", "Nước ngoài"]
        )
        ghi_chu = st.text_area("Ghi chú", placeholder="Nhập ghi chú (nếu có)", height=100)

    btn_submit = st.form_submit_button("Thêm khách hàng")

# Xử lý khi bấm nút "Thêm khách hàng"
if btn_submit:
    if not sdt.strip() or not ten.strip():
        st.error("Vui lòng điền đầy đủ **Số điện thoại** và **Tên khách hàng**!")
    else:
        thong_tin_moi = pd.DataFrame([{
            "Số điện thoại": sdt.strip(),
            "Tên khách hàng": ten.strip(),
            "Khu vực": khu_vuc,
            "Ghi chú": ghi_chu.strip()
        }])
        
        # Cập nhật dữ liệu
        st.session_state.df_khach_hang = pd.concat(
            [st.session_state.df_khach_hang, thong_tin_moi], 
            ignore_index=True
        )
        st.success(f"Đã thêm thành công khách hàng: **{ten}**!")

st.divider()

# Hiển thị danh sách khách hàng
st.subheader("📑 Danh sách khách hàng đã nhập")
st.dataframe(st.session_state.df_khach_hang, use_container_width=True)

# Tải danh sách về file Excel
if not st.session_state.df_khach_hang.empty:
    @st.cache_data
    def convert_df_to_excel(df):
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="KhachHang")
        return output.getvalue()

    excel_data = convert_df_to_excel(st.session_state.df_khach_hang)
    
    st.download_button(
        label="📥 Tải danh sách (Excel)",
        data=excel_data,
        file_name="danh_sach_khach_hang.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
