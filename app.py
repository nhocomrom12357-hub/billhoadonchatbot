import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime
import os
import json
import unicodedata
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
 
 
# =========================================================
# CẤU HÌNH TRANG
# =========================================================
 
st.set_page_config(
   page_title="Tính Bill Trà Sữa",
   page_icon="🧋",
   layout="centered"
)
 
st.image("IMG_5982.png", use_container_width=True)
 
 
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
 
def pdf_safe_text(value):
   """Chuyển chữ tiếng Việt thành ASCII để font Helvetica mặc định đọc được."""
   value = str(value).replace("Đ", "D").replace("đ", "d")
   normalized = unicodedata.normalize("NFKD", value)
   return "".join(
       character
       for character in normalized
       if not unicodedata.combining(character) and ord(character) < 128
   )
 
 
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
       # Helvetica mặc định không hỗ trợ dấu tiếng Việt.
       customer_name = pdf_safe_text(customer_name)
 
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
 
       drink_name = item["drink"] if font_path else pdf_safe_text(item["drink"])
       quantity = item["quantity"]
       price = item["price"]
       toppings = item["toppings"] if font_path else [pdf_safe_text(topping) for topping in item["toppings"]]
       sugar = item["sugar"] if font_path else pdf_safe_text(item["sugar"])
       ice = item["ice"] if font_path else pdf_safe_text(item["ice"])
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
       f"TONG THANH TOAN: {total_money:,.0f} VND",
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
                   "**Topping:** Không")
 
 
           # Hiển thị mức đường, mức đá và hoàn tất phần hóa đơn
           st.write(f"**Mức đường:** {item['sugar']}  |  **Mức đá:** {item['ice']}")
 
       st.divider()
       st.subheader(f"💰 TỔNG THANH TOÁN: {format_money(total_money)}")
 
       pdf_data = create_pdf(customer_name, order_items, total_money, invoice_number)
       st.download_button(
           "📄 TẢI HÓA ĐƠN PDF",
           data=pdf_data,
           file_name=f"hoa_don_{invoice_number}.pdf",
           mime="application/pdf",
           use_container_width=True
       )
 
 
# =========================================================
# CHATBOT TƯ VẤN MENU
# =========================================================
st.divider()
st.subheader("💬 Chatbot tư vấn trà sữa")
st.caption("Hỏi chatbot về món, giá, topping hoặc nhờ gợi ý đồ uống.")
 
# Chỉ giữ hội thoại chatbot trong session hiện tại.
if "chat_messages" not in st.session_state:
   st.session_state.chat_messages = []
 
for message in st.session_state.chat_messages:
   with st.chat_message(message["role"]):
       st.markdown(message["content"])
 
user_prompt = st.chat_input("Ví dụ: Món nào ít ngọt, giá dưới 35.000đ?")
if user_prompt:
   st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
   with st.chat_message("user"):
       st.markdown(user_prompt)
 
   # Lấy khóa từ .streamlit/secrets.toml, không ghi khóa vào mã nguồn.
   try:
       api_key = st.secrets["OPENROUTER_API_KEY"]
   except Exception:
       api_key = None
 
   if not api_key:
       reply = (
           "Chưa cấu hình API key. Tạo file `.streamlit/secrets.toml` cạnh `app.py` "
           "với nội dung `OPENROUTER_API_KEY = \"khóa_mới_của_bạn\"`, rồi chạy lại ứng dụng."
       )
   else:
       menu_text = "\n".join(f"- {name}: {price:,} VNĐ" for name, price in MENU.items())
       toppings_text = "\n".join(f"- {name}: {price:,} VNĐ" for name, price in TOPPINGS.items())
       system_prompt = (
           "Bạn là nhân viên tư vấn thân thiện của quán trà sữa. Trả lời bằng tiếng Việt ngắn gọn. "
           "Chỉ tư vấn từ menu và giá bên dưới; không tự bịa món, giá hay thông tin sức khỏe. "
           "Nếu khách hỏi ngoài menu, hãy nói rõ và gợi ý món gần nhất.\n\n"
           f"MENU:\n{menu_text}\n\nTOPPING (giá cộng thêm cho mỗi ly):\n{toppings_text}\n\n"
           "Mức đường/đá có thể chọn: 100%, 70%, 0%."
       )
       payload = {
           "model": "openrouter/auto",
           "messages": [
               {"role": "system", "content": system_prompt},
               *st.session_state.chat_messages[-12:]
           ],
           "temperature": 0.7,
           "max_tokens": 500
       }
       request = Request(
           "https://openrouter.ai/api/v1/chat/completions",
           data=json.dumps(payload).encode("utf-8"),
           headers={
               "Authorization": f"Bearer {api_key}",
               "Content-Type": "application/json",
               "HTTP-Referer": "http://localhost:8501",
               "X-Title": "Chatbot tu van tra sua"
           },
           method="POST"
       )
       try:
           with urlopen(request, timeout=45) as response:
               result = json.loads(response.read().decode("utf-8"))
           reply = result["choices"][0]["message"]["content"].strip()
       except HTTPError as error:
           detail = error.read().decode("utf-8", errors="replace")[:500]
           reply = f"OpenRouter báo lỗi {error.code}. Kiểm tra API key/tài khoản rồi thử lại.\n\nChi tiết: {detail}"
       except (URLError, TimeoutError, KeyError, IndexError, ValueError) as error:
           reply = f"Chưa nhận được câu trả lời từ chatbot. Bạn thử lại nhé. ({error})"
 
   st.session_state.chat_messages.append({"role": "assistant", "content": reply})
   with st.chat_message("assistant"):
       st.markdown(reply)
