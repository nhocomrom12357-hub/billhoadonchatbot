import streamlit as st
st.image("IMG_6152.jpeg", use_container_width=True)
from fpdf import FPDF
from io import BytesIO
from datetime import datetime
import os
import re


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)


# =========================================================
# DỮ LIỆU MENU
# =========================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa bạc hà": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Thạch phô mai": 7000,
    "Kem cheese": 10000,
}


SUGAR_LEVELS = [
    "100%",
    "70%",
    "0%"
]

ICE_LEVELS = [
    "100%",
    "70%",
    "0%"
]


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(number):
    return f"{number:,.0f} VNĐ"


# =========================================================
# HÀM TẠO SỐ HÓA ĐƠN
# =========================================================

def create_invoice_number():
    return datetime.now().strftime("HD%Y%m%d%H%M%S")


# =========================================================
# HÀM TẠO FILE PDF
# =========================================================

def create_pdf(customer_name, order_items, total_money, invoice_number):

    pdf = FPDF()
    pdf.add_page()
    

    # Nếu tìm thấy font Unicode
    if font_path:
        pdf.add_font(
            "DejaVu",
            "",
            font_path
        )
        pdf.add_font(
            "DejaVu",
            "B",
            font_path
        )

        normal_font = "DejaVu"
        bold_font = "DejaVu"
    else:
        normal_font = "Helvetica"
        bold_font = "Helvetica"

    # =====================================================
    # TIÊU ĐỀ
    # =====================================================

    pdf.set_font(
        bold_font,
        size=18
    )

    pdf.cell(
        0,
        10,
        "HOA DON QUAN TRA SUA",
        align="C"
    )

    pdf.ln(12)

    # =====================================================
    # THÔNG TIN HÓA ĐƠN
    # =====================================================

    pdf.set_font(
        normal_font,
        size=11
    )

    pdf.cell(
        0,
        7,
        f"So hoa don: {invoice_number}"
    )

    pdf.ln(7)

    pdf.cell(
        0,
        7,
        f"Khach hang: {customer_name}"
    )

    pdf.ln(7)

    pdf.cell(
        0,
        7,
        datetime.now().strftime(
            "Thoi gian: %d/%m/%Y %H:%M"
        )
    )

    pdf.ln(10)

    # =====================================================
    # DANH SÁCH MÓN
    # =====================================================

    pdf.set_font(
        bold_font,
        size=11
    )

    pdf.cell(60, 8, "Mon", border=1)
    pdf.cell(15, 8, "SL", border=1, align="C")
    pdf.cell(35, 8, "Don gia", border=1, align="C")
    pdf.cell(70, 8, "Thanh tien", border=1, align="C")

    pdf.ln(8)

    pdf.set_font(
        normal_font,
        size=9
    )

    for item in order_items:

        drink_name = item["drink"]
        quantity = item["quantity"]
        price = item["price"]
        toppings = item["toppings"]
        sugar = item["sugar"]
        ice = item["ice"]
        subtotal = item["subtotal"]

        pdf.cell(
            60,
            8,
            drink_name,
            border=1
        )

        pdf.cell(
            15,
            8,
            str(quantity),
            border=1,
            align="C"
        )

        pdf.cell(
            35,
            8,
            f"{price:,.0f}",
            border=1,
            align="C"
        )

        pdf.cell(
            70,
            8,
            f"{subtotal:,.0f}",
            border=1,
            align="C"
        )

        pdf.ln(8)

        # Topping
        if toppings:
            topping_text = "Topping: " + ", ".join(toppings)

            pdf.multi_cell(
                180,
                6,
                topping_text
            )

        pdf.cell(
            180,
            6,
            f"Duong: {sugar} | Da: {ice}"
        )

        pdf.ln(7)

    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    pdf.ln(5)

    pdf.set_font(
        bold_font,
        size=14
    )

    pdf.cell(
        0,
        10,
        f"TONG THANH TOAN: {total_money:,.0f} VNĐ",
        align="R"
    )

    pdf.ln(15)

    pdf.set_font(
        normal_font,
        size=10
    )

    pdf.cell(
        0,
        7,
        "Cam on quy khach! Hen gap lai.",
        align="C"
    )

    # Xuất PDF ra bộ nhớ
    pdf_bytes = bytes(pdf.output())

    return pdf_bytes


# =========================================================
# GIAO DIỆN
# =========================================================

st.title("🧋 QUÁN TRÀ SỮA")

st.subheader("🧾 TÍNH BILL HÓA ĐƠN")

st.write(
    "Nhập thông tin khách hàng và các món khách đã gọi."
)

st.divider()


# =========================================================
# TÊN KHÁCH HÀNG
# =========================================================

customer_name = st.text_input(
    "👤 Tên khách hàng",
    placeholder="Ví dụ: Nguyễn Văn An"
)


# =========================================================
# NHẬP CÁC MÓN
# =========================================================

st.subheader("🧋 Chọn món")

order_items = []


# Cho phép tối đa 5 món trong một hóa đơn
for i in range(5):

    st.markdown(f"### Món {i + 1}")

    col1, col2 = st.columns(2)

    with col1:

        drink = st.selectbox(
            "Loại trà sữa",
            ["-- Không chọn --"] + list(MENU.keys()),
            key=f"drink_{i}"
        )

    with col2:

        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
            key=f"quantity_{i}"
        )

    col3, col4 = st.columns(2)

    with col3:

        sugar = st.selectbox(
            "🍬 Mức đường",
            SUGAR_LEVELS,
            key=f"sugar_{i}"
        )

    with col4:

        ice = st.selectbox(
            "🧊 Mức đá",
            ICE_LEVELS,
            key=f"ice_{i}"
        )

    toppings = st.multiselect(
        "🍮 Topping",
        list(TOPPINGS.keys()),
        key=f"toppings_{i}"
    )

    st.divider()

    # Nếu người dùng chọn món
    if drink != "-- Không chọn --":

        drink_price = MENU[drink]

        topping_price = sum(
            TOPPINGS[topping]
            for topping in toppings
        )

        price_per_item = drink_price + topping_price

        subtotal = price_per_item * quantity

        order_items.append({
            "drink": drink,
            "quantity": quantity,
            "price": price_per_item,
            "drink_price": drink_price,
            "toppings": toppings,
            "topping_price": topping_price,
            "sugar": sugar,
            "ice": ice,
            "subtotal": subtotal
        })


# =========================================================
# TÍNH TỔNG TIỀN
# =========================================================

total_money = sum(
    item["subtotal"]
    for item in order_items
)


# =========================================================
# NÚT THANH TOÁN
# =========================================================

if st.button(
    "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
    use_container_width=True
):

    # Kiểm tra tên khách
    if not customer_name.strip():

        st.error(
            "⚠️ Vui lòng nhập tên khách hàng."
        )

    # Kiểm tra có món hay chưa
    elif len(order_items) == 0:

        st.error(
            "⚠️ Vui lòng chọn ít nhất một món."
        )

    else:

        invoice_number = create_invoice_number()

        # =================================================
        # HIỂN THỊ KẾT QUẢ
        # =================================================

        st.success(
            "✅ Thanh toán thành công!"
        )

        st.divider()

        st.subheader("🧾 THÔNG TIN HÓA ĐƠN")

        st.write(
            f"**👤 Khách hàng:** {customer_name}"
        )

        st.write(
            f"**🔢 Số hóa đơn:** {invoice_number}"
        )

        st.write(
            datetime.now().strftime(
                "**🕐 Thời gian:** %d/%m/%Y %H:%M:%S"
            )
        )

        st.divider()

        # =================================================
        # HIỂN THỊ CÁC MÓN
        # =================================================

        for index, item in enumerate(order_items):

            st.markdown(
                f"### 🧋 {index + 1}. {item['drink']}"
            )

            st.write(
                f"**Số lượng:** {item['quantity']}"
            )

            st.write(
                f"**Giá trà:** {format_money(item['drink_price'])}"
            )

            if item["toppings"]:

                st.write(
                    "**Topping:** "
                    + ", ".join(item["toppings"])
                )

                st.write(
                    f"**Tiền topping:** "
                    f"{format_money(item['topping_price'])}"
                )

            else:

                st.write(
                    "**Topping:** Không"
                )

            st.write(
                f"**Đường:** {item['sugar']}"
            )

            st.write(
                f"**Đá:** {item['ice']}"
            )

            st.write(
                f"**Thành tiền:** "
                f"**{format_money(item['subtotal'])}**"
            )

            st.divider()

        # =================================================
        # TỔNG TIỀN
        # =================================================

        st.subheader(
            f"💰 TỔNG THANH TOÁN: {format_money(total_money)}"
        )

        # =================================================
        # TẠO FILE PDF
        # =================================================

        pdf_file = create_pdf(
            customer_name,
            order_items,
            total_money,
            invoice_number
        )

        # =================================================
        # NÚT TẢI HÓA ĐƠN
        # =================================================

        safe_customer_name = re.sub(
            r"[^a-zA-Z0-9_]+",
            "_",
            customer_name
        )

        file_name = (
            f"HoaDon_{invoice_number}_"
            f"{safe_customer_name}.pdf"
        )

        st.download_button(
            label="📥 TẢI HÓA ĐƠN PDF",
            data=pdf_file,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )
