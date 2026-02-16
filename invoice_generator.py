import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
import io
from datetime import date

# --- Page Setup ---
st.set_page_config(page_title="Elite Invoice Generator", layout="wide")
st.title("📑 Professional Sales Invoice Maker")

# --- Sidebar: Company & Logo ---
with st.sidebar:
    st.header("🏢 Your Company Details")
    logo_file = st.file_uploader("Upload Company Logo", type=['jpg', 'png', 'jpeg'])
    company_name = st.text_input("Company Name", "MG MOTORS")
    company_addr = st.text_area("Address", "SHOP NO-1, NILKANTH VILLA, SURAT")
    company_mob = st.text_input("Mobile", "8200575486")
    
    st.divider()
    st.header("🏦 Bank Details")
    bank_name = st.text_input("Bank Name", "Bank of Baroda")
    acc_no = st.text_input("Account Number", "02810100054800")
    ifsc = st.text_input("IFSC Code", "BARB0UDHNAX")

# --- Main UI: Customer & Invoice Info ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("👤 Customer Details")
    cust_name = st.text_input("Customer/Business Name", "AGARWAL ENTERPRISE")
    cust_mob = st.text_input("Customer Mobile", "9998944200")
    vehicle_no = st.text_input("Vehicle Number (Optional)", "GJ05BY9222")

with col2:
    st.subheader("📄 Invoice Info")
    inv_no = st.text_input("Invoice Number", "495")
    inv_date = st.date_input("Invoice Date", date.today())

# --- Items Table ---
st.subheader("🛒 Items & Services")
if 'items' not in st.session_state:
    st.session_state.items = [{"desc": "", "qty": 1, "rate": 0.0}]

def add_item():
    st.session_state.items.append({"desc": "", "qty": 1, "rate": 0.0})

for i, item in enumerate(st.session_state.items):
    c1, c2, c3 = st.columns([3, 1, 1])
    st.session_state.items[i]['desc'] = c1.text_input(f"Description {i+1}", item['desc'], key=f"desc_{i}")
    st.session_state.items[i]['qty'] = c2.number_input(f"Qty {i+1}", min_value=1, value=item['qty'], key=f"qty_{i}")
    st.session_state.items[i]['rate'] = c3.number_input(f"Rate {i+1}", min_value=0.0, value=item['rate'], key=f"rate_{i}")

st.button("➕ Add More Item", on_click=add_item)

# --- PDF Generation Logic ---
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []

    # Logo & Header
    if logo_file:
        img = Image(logo_file, width=25*mm, height=25*mm)
        story.append(img)
    
    story.append(Paragraph(f"<b>{company_name}</b>", styles['Title']))
    story.append(Paragraph(f"{company_addr}<br/>Mobile: {company_mob}", styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<hr/>", styles['Normal']))
    
    # Invoice & Customer Info Table
    info_data = [
        [f"BILL TO: {cust_name}", f"Invoice No: {inv_no}"],
        [f"Mobile: {cust_mob}", f"Date: {inv_date}"],
        [f"Vehicle: {vehicle_no}", ""]
    ]
    info_table = Table(info_data, colWidths=[100*mm, 60*mm])
    story.append(info_table)
    story.append(Spacer(1, 15))

    # Items Table
    table_data = [["Description", "Qty", "Rate", "Amount"]]
    total = 0
    for item in st.session_state.items:
        amt = item['qty'] * item['rate']
        total += amt
        table_data.append([item['desc'], str(item['qty']), f"{item['rate']:.2f}", f"{amt:.2f}"])
    
    table_data.append(["", "", "Total Amount:", f"Rs. {total:.2f}"])
    
    t = Table(table_data, colWidths=[80*mm, 20*mm, 30*mm, 30*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -2), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t)
    
    # Bank Details
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>Bank Details:</b>", styles['Normal']))
    story.append(Paragraph(f"Bank: {bank_name} | A/c: {acc_no} | IFSC: {ifsc}", styles['Normal']))
    
    doc.build(story)
    return buffer.getvalue()

# --- Download Button ---
st.divider()
if st.button("🚀 Generate & Download Invoice"):
    pdf_out = generate_pdf()
    st.download_button(label="📥 Download PDF", data=pdf_out, file_name=f"Invoice_{inv_no}.pdf", mime="application/pdf")
