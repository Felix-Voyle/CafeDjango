import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def invoice_header(can, cafe_info):
    can.drawString(45, 760, cafe_info["name"])
    can.drawString(510, 760, "INVOICE")
    can.setFont("Helvetica", 8)
    can.drawString(45, 745, cafe_info["address"])


def invoice_footer(can, cafe_info):
    # Draw thin black horizontal line just above the footer text
    can.setStrokeColorRGB(0, 0, 0)
    can.setLineWidth(1)
    can.line(45, 150, 565, 150)

    can.setFont("Helvetica-Bold", 9)
    # Draw footer headers
    can.drawString(45, 120, cafe_info["name"])  # Position of the footer text
    can.drawString(240, 120, "Contact Information")
    can.drawString(410, 120, "Payment Details")

    can.setFont("Helvetica", 8)
    # Draw company details
    can.drawString(45, 100, cafe_info["address"])
    can.drawString(45, 85, "Company Number: " + cafe_info["company_number"])
    can.drawString(45, 70, "VAT Number: " + cafe_info["vat_number"])

    # Draw contact information
    can.drawString(240, 100, cafe_info["contact"])
    can.drawString(240, 85, cafe_info["phone"])
    can.drawString(240, 70, cafe_info["email"])

    # Draw payment details
    can.drawString(410, 100, "IBAN: " + cafe_info["iban"])
    can.drawString(410, 85, "Bank: " + cafe_info["bank"])
    can.drawString(410, 70, "Sort code: " + cafe_info["sort_code"])
    can.drawString(410, 55, "Account holder: " + cafe_info["account_holder"])
    can.drawString(410, 40, "Bank account: " + cafe_info["account_number"])


def recipient_information(can, recipient_info):
    # Draw recipient information
    recipient_y_coordinate = 720
    for line in recipient_info:
        if line is not None:
            can.drawString(45, recipient_y_coordinate, line)
            recipient_y_coordinate -= 10


def invoice_information(can, additional_info):
    # Draw additional information on the right-hand side
    info_x_coordinate = 465
    info_y_coordinate = 720  # Align with recipient info
    for line in additional_info:
        can.drawString(info_x_coordinate, info_y_coordinate, line)
        info_y_coordinate -= 10


def specify_order(can, order_detail):
    can.drawString(250, 660, order_detail)

def draw_table_header(can):
    # Draw pale grey rectangle as the background for the header
    can.setFillColorRGB(0.9, 0.9, 0.9)
    can.rect(40, 625 + 5, 525, 15, fill=1)

    # Set font and color for the header text
    can.setFillColorRGB(0, 0, 0)  # Set text color to black
    can.setFont("Helvetica", 8)  # Set font to bold and size to 10

    # Draw header text
    can.drawString(45, 635, "Description")
    can.drawString(275, 635, "Quantity")
    can.drawString(414, 635, "Price")
    can.drawString(526, 635, "Subtotal")


def order_information(can, cart, start_index, end_index):
    y_coordinate = 600

    for i in range(start_index, end_index):
        item = cart[i]
        description = item["description"]
        quantity = item["quantity"]
        price = item["price"]
        subtotal = item["subtotal"]

        # Write the item details to the PDF
        can.drawString(45, y_coordinate, description)
        can.drawString(285, y_coordinate, str(quantity))
        can.drawString(415, y_coordinate, str(price))
        can.drawString(530, y_coordinate, str(subtotal))

        # Update y-coordinate for the next item
        y_coordinate -= 15
    return y_coordinate


def invoice_totals(can, y_coordinate, totals):
    can.setStrokeColorRGB(0, 0, 0)
    can.setLineWidth(0.5)
    can.line(45, y_coordinate, 565, y_coordinate)
    y_coordinate -= 15

    for label, value in totals.items():
        can.drawString(415, y_coordinate, label)  # Draw the label
        can.drawString(530, y_coordinate, str(value))  # Draw the value

        # Draw a horizontal line after the label and value
        y_coordinate -= 5  # Adjust for spacing
        can.line(415, y_coordinate, 555, y_coordinate)
        y_coordinate -= 10  # Adjust for spacing between lines


def generate_invoice(recipient_info, order_info, cart, totals, order_detail=None, cafe_info=None):
    # Create a BytesIO object to store the PDF content
    pdf_buffer = io.BytesIO()
    
    # Create a canvas object for each page and add content to it
    can = canvas.Canvas(pdf_buffer, pagesize=letter)
    num_items = len(cart)
    items_per_page = 25

    for page_num in range((num_items + items_per_page - 1) // items_per_page):
        start_index = page_num * items_per_page
        end_index = min((page_num + 1) * items_per_page, num_items)
        
        # Add content to the canvas for each page
        invoice_header(can, cafe_info)
        invoice_footer(can, cafe_info)
        recipient_information(can, recipient_info)
        invoice_information(can, order_info)
        if order_detail is not None:
            specify_order(can, order_detail)
        draw_table_header(can)
        y_coordinate = order_information(can, cart, start_index, end_index)
        if page_num == (num_items + items_per_page - 1) // items_per_page - 1:
            invoice_totals(can, y_coordinate, totals)
        
        # Save the canvas content for each page
        can.showPage()

    # Save the canvas content to the PDF buffer
    can.save()

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer
