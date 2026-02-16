from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib import colors
import datetime

def generate_invoice(filename="elite_invoice.pdf", invoice_data=None):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='InvoiceHeader', fontName='Helvetica-Bold', fontSize=24, alignment=TA_CENTER, textColor=colors.HexColor('#1a73e8')))
    styles.add(ParagraphStyle(name='CompanyInfo', fontName='Helvetica-Bold', fontSize=12, alignment=TA_RIGHT, textColor=colors.black))
    styles.add(ParagraphStyle(name='AddressInfo', fontName='Helvetica', fontSize=10, alignment=TA_RIGHT, textColor=colors.gray))
    styles.add(ParagraphStyle(name='InvoiceDetails', fontName='Helvetica-Bold', fontSize=10, alignment=TA_RIGHT, textColor=colors.HexColor('#1a73e8')))
    styles.add(ParagraphStyle(name='ClientHeader', fontName='Helvetica-Bold', fontSize=12, textColor=colors.black))
    styles.add(ParagraphStyle(name='ClientInfo', fontName='Helvetica', fontSize=10, textColor=colors.black))
    styles.add(ParagraphStyle(name='TableHeader', fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER, textColor=colors.white))
    styles.add(ParagraphStyle(name='TableData', fontName='Helvetica', fontSize=9, alignment=TA_CENTER, textColor=colors.black))
    styles.add(ParagraphStyle(name='TableDataRight', fontName='Helvetica', fontSize=9, alignment=TA_RIGHT, textColor=colors.black))
    styles.add(ParagraphStyle(name='TotalLabel', fontName='Helvetica-Bold', fontSize=10, alignment=TA_RIGHT, textColor=colors.black))
    styles.add(ParagraphStyle(name='TotalValue', fontName='Helvetica-Bold', fontSize=12, alignment=TA_RIGHT, textColor=colors.HexColor('#1a73e8')))

    story = []

    # --- 1. Invoice Header (Elite PDF Editor) ---
    story.append(Paragraph("ELITE INVOICE", styles['InvoiceHeader']))
    story.append(Spacer(1, 5*mm))

    # --- 2. Company Info (Right Aligned) ---
    story.append(Paragraph("Your Company Name Pvt. Ltd.", styles['CompanyInfo']))
    story.append(Paragraph("123, Elite Street, Cyber City", styles['AddressInfo']))
    story.append(Paragraph("Gandhinagar, Gujarat - 382007", styles['AddressInfo']))
    story.append(Paragraph("GSTIN: 24ABCDE1234F1Z5", styles['AddressInfo']))
    story.append(Paragraph("Email: info@elitepdf.com | Phone: +91 9876543210", styles['AddressInfo']))
    story.append(Spacer(1, 10*mm))

    # --- 3. Invoice Details (Date, Invoice No.) ---
    invoice_num = invoice_data.get('invoice_number', 'INV-2023-001')
    invoice_date = invoice_data.get('invoice_date', datetime.date.today().strftime("%d-%m-%Y"))
    due_date = invoice_data.get('due_date', (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d-%m-%Y"))

    details_data = [
        [Paragraph(f"<b>Invoice No:</b> {invoice_num}", styles['InvoiceDetails'])],
        [Paragraph(f"<b>Invoice Date:</b> {invoice_date}", styles['InvoiceDetails'])],
        [Paragraph(f"<b>Due Date:</b> {due_date}", styles['InvoiceDetails'])],
    ]
    details_table = Table(details_data, colWidths=[80*mm])
    details_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 5*mm))

    # --- 4. Bill To / Client Details ---
    story.append(Paragraph("Bill To:", styles['ClientHeader']))
    story.append(Paragraph(invoice_data.get('client_name', "Client Name Inc."), styles['ClientInfo']))
    story.append(Paragraph(invoice_data.get('client_address', "Client Address Line 1"), styles['ClientInfo']))
    story.append(Paragraph(invoice_data.get('client_city_zip', "Client City, PIN-123456"), styles['ClientInfo']))
    story.append(Paragraph(invoice_data.get('client_gstin', "Client GSTIN: XYZABC1234P1Z3"), styles['ClientInfo']))
    story.append(Spacer(1, 15*mm))

    # --- 5. Item Table ---
    item_table_data = [
        [
            Paragraph("S.No.", styles['TableHeader']),
            Paragraph("Description", styles['TableHeader']),
            Paragraph("Qty", styles['TableHeader']),
            Paragraph("Rate", styles['TableHeader']),
            Paragraph("Amount", styles['TableHeader'])
        ]
    ]
    
    items = invoice_data.get('items', [])
    subtotal = 0
    for i, item in enumerate(items):
        amount = item['qty'] * item['rate']
        subtotal += amount
        item_table_data.append([
            Paragraph(str(i+1), styles['TableData']),
            Paragraph(item['description'], styles['TableData']),
            Paragraph(str(item['qty']), styles['TableData']),
            Paragraph(f"₹ {item['rate']:.2f}", styles['TableDataRight']),
            Paragraph(f"₹ {amount:.2f}", styles['TableDataRight'])
        ])

    item_table = Table(item_table_data, colWidths=[10*mm, 85*mm, 20*mm, 30*mm, 35*mm])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a73e8')), # Header Background
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')), # Table Borders
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ]))
    story.append(item_table)
    story.append(Spacer(1, 10*mm))

    # --- 6. Totals Section ---
    gst_rate = 0.18 # 18% GST
    gst_amount = subtotal * gst_rate
    total_amount = subtotal + gst_amount

    totals_data = [
        [Paragraph("Subtotal:", styles['TotalLabel']), Paragraph(f"₹ {subtotal:.2f}", styles['TableDataRight'])],
        [Paragraph(f"GST ({gst_rate*100:.0f}%):", styles['TotalLabel']), Paragraph(f"₹ {gst_amount:.2f}", styles['TableDataRight'])],
        [Paragraph("Total Amount:", styles['TotalValue']), Paragraph(f"₹ {total_amount:.2f}", styles['TotalValue'])],
    ]
    totals_table = Table(totals_data, colWidths=[120*mm, 50*mm])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 15*mm))

    # --- 7. Notes / Terms ---
    story.append(Paragraph("<b>Terms & Conditions:</b>", styles['ClientHeader']))
    story.append(Paragraph("1. Payment is due within 7 days of invoice date.", styles['ClientInfo']))
    story.append(Paragraph("2. Late payments will incur a 2% monthly interest.", styles['ClientInfo']))
    story.append(Spacer(1, 20*mm))
    
    # --- 8. Authorized Signature ---
    story.append(Paragraph("For Your Company Name Pvt. Ltd.", styles['CompanyInfo']))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("________________________", styles['CompanyInfo']))
    story.append(Paragraph("(Authorized Signature)", styles['AddressInfo']))


    doc.build(story)

# --- Example Usage ---
if __name__ == "__main__":
    example_invoice_data = {
        "invoice_number": "INV-ELITE-2024-007",
        "invoice_date": "22-07-2024",
        "due_date": "29-07-2024",
        "client_name": "Tech Solutions Hub",
        "client_address": "456, Innovation Drive",
        "client_city_zip": "Bengaluru, Karnataka - 560001",
        "client_gstin": "29AABBCC1234D1Z6",
        "items": [
            {"description": "Web Development Services", "qty": 1, "rate": 25000.00},
            {"description": "Monthly SEO Package", "qty": 2, "rate": 5000.00},
            {"description": "Graphic Design Consultation", "qty": 1, "rate": 3000.00}
        ]
    }
    generate_invoice("my_elite_invoice.pdf", example_invoice_data)
    print("Elite Invoice generated: my_elite_invoice.pdf")
