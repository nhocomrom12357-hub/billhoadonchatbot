import streamlit as st
st.image("IMG_5982.png", use_container_width=True)
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

    # Tìm font Unicode
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
    ]

    font_path = None

    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break

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
                    "**Topping:** Không")
