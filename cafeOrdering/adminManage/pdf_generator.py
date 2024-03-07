import io
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def invoice_header(can):
    can.drawString(45, 760, "JAVA JAVA COFFEE")
    can.drawString(510, 760, "INVOICE")
    can.setFont("Helvetica", 8)
    can.drawString(45, 745, "160 Fleet Street, London, EC4A 2DQ")


def invoice_footer(can):
    # Draw thin black horizontal line just above the footer text
    can.setStrokeColorRGB(0, 0, 0)
    can.setLineWidth(1) 
    can.line(45, 150, 565, 150) 

    can.setFont("Helvetica-Bold", 9)
    # Draw footer headers
    can.drawString(45, 120, "Java Java Coffee")  # Position of the footer text
    can.drawString(240, 120, "Contact Information")
    can.drawString(410, 120, "Payment Details")

    can.setFont("Helvetica", 8)
    # Draw company details
    can.drawString(45, 100, "160 Fleet Street, London EC4A 2DQ")
    can.drawString(45, 85, "Company Number: 09372930")
    can.drawString(45, 70, "VAT Number: 275783947")

    # Draw contact information
    can.drawString(240, 100, "Jonathan Hynes")
    can.drawString(240, 85, "+447585942273")
    can.drawString(240, 70, "Javajavacoffee@hotmail.com")

    # Draw payment details 
    can.drawString(410, 100, "IBAN: GB03HBUK40361611552082")
    can.drawString(410, 85, "Bank: HSBC")
    can.drawString(410, 70, "Sort code: 403616")
    can.drawString(410, 55, "Account holder: Java Java London Limited")
    can.drawString(410, 40, "Bank account: 11552082")


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
    can.drawString(250, 660, "Catering @ Record Hall")


def draw_table_header(can):
    # Draw pale grey rectangle as the background for the header
    can.setFillColorRGB(0.9, 0.9, 0.9) 
    can.rect(40, 625 + 5, 525, 15, fill=1)

    # Set font and color for the header text
    can.setFillColorRGB(0, 0, 0)  # Set text color to black
    can.setFont("Helvetica", 8)  # Set font to bold and size to 10

    # Draw header text
    can.drawString(45, 635, "Description")
    can.drawString(285, 635, "Quantity")
    can.drawString(415, 635, "Price")
    can.drawString(530, 635, "Subtotal")


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
        can.line(415, y_coordinate, 550, y_coordinate)
        y_coordinate -= 10  # Adjust for spacing between lines


def generate_invoice(recipient_info, order_info, cart):
    # Create a PdfWriter object to store the pages
    output_pdf = PdfWriter()

    # Create a canvas object for each page and add content to it
    num_items = len(cart)  # Example: Total number of items
    items_per_page = 25

    for page_num in range((num_items + items_per_page - 1) // items_per_page):  # Calculate the number of pages
        start_index = page_num * items_per_page
        end_index = min((page_num + 1) * items_per_page, num_items)  # Ensure not to exceed total number of items
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        invoice_header(can)
        invoice_footer(can)
        recipient_information(can, recipient_info)
        invoice_information(can, order_info)
        draw_table_header(can)
        y_coordinate = order_information(can, cart, start_index, end_index)  # Add numbers specific to each page
        #if page_num == (num_items + items_per_page - 1) // items_per_page - 1:
            #invoice_totals(can, y_coordinate, totals)
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)

        output_pdf.add_page(new_pdf.pages[0])  # Add the page to the output PDF

    # Write the output PDF to a file
    with open("output.pdf", "wb") as output_stream:
        output_pdf.write(output_stream)


