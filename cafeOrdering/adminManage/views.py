# Standard library imports
import json
from decimal import Decimal, ROUND_HALF_UP
import random
import tempfile
import os
import base64


# Third-party library imports
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import FileResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# Local application imports
from .pdf_generator import generate_invoice
from enquire.models import Enquiry
from order.models import Order
from products.models import InvoiceProduct


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def manage(request):
    enquiries = Enquiry.objects.all()
    orders = Order.objects.filter(delivery_date__gte=timezone.now()).order_by('delivery_date')

    items_per_page = 15

    paginator = Paginator(orders, items_per_page)

    page_number = request.GET.get('page')
    
    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    ctx = {
        'enquiries': enquiries,
        'orders': orders,
    }

    return render(request, 'adminManage/manage.html', ctx)


def filter_orders(request):
    status = request.GET.get('status')
    enquiries = Enquiry.objects.all()
    if status in dict(Order.ORDER_STATUS):
        orders = Order.objects.filter(status=status).order_by('delivery_date')
    elif status == "all":
        orders = Order.objects.order_by('delivery_date')
    else:
        orders = Order.objects.filter(delivery_date__gte=timezone.now()).order_by('delivery_date')
    

    items_per_page = 15
    paginator = Paginator(orders, items_per_page)
    page_number = request.GET.get('page')

    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    ctx = {
        'orders': orders,
        'enquiries': enquiries,
    }

    return render(request, 'adminManage/manage.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def enquiries(request):
    enquiries = Enquiry.objects.all()
    
    ctx = {
        'enquiries': enquiries,
    }

    return render(request, 'adminManage/enquiries.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def enquiry(request, enquiry_id):
    enquiries = Enquiry.objects.all()
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    enquiry.viewed = True
    enquiry.save()
    ctx = {
        'enquiry': enquiry,
        'enquiries': enquiries,
    }

    return render(request, 'adminManage/enquiry.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def delete_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)

    try:
        enquiry.delete()
        messages.success(request, "Enquiry Deleted")
    except Enquiry.DoesNotExist:
        messages.error(request, f"Could not find enquiry {enquiry_id}")

    return HttpResponseRedirect(reverse('enquiries'))


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def create_invoice(request):
    products = InvoiceProduct.objects.all()
    enquiries = Enquiry.objects.all()
    order_reference = ''.join(random.choices('0123456789', k=5))
    invoice_items = []

    ctx = {
        'products': products,
        'enquiries': enquiries,
    }

    if request.method == 'POST':
        product_ids = request.POST.getlist('products')
        quantities = request.POST.getlist('quantities')
        business_name = request.POST.get('business_name')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        address_line3 = request.POST.get('address_line3')
        postcode = request.POST.get('postcode')
        invoice_date = request.POST.get('invoice_date')
        order_detail = request.POST.get('order_detail')

        recipient_info = [
            business_name,
            address_line1,
            address_line2,
            address_line3,
            postcode,
        ]

        order_info = [
            "Order Reference: " + order_reference,
            "Invoice Date: " + invoice_date,
            "Payment Terms: 30 days",
            ]

        for product_id, quantity in zip(product_ids, quantities):
            try:
                product = InvoiceProduct.objects.get(pk=product_id)
                price = product.price  
                subtotal = int(quantity) * price
                product_info = {
                    "description": product.name,
                    "quantity": int(quantity),
                    "price": price,
                    "subtotal": subtotal,
                }

                invoice_items.append(product_info)
            except InvoiceProduct.DoesNotExist:
                messages.error(request, f"Product {product.name} does not exist")
                return redirect('create_invoice')
        
        order_total = sum(item['subtotal'] for item in invoice_items)
        discount_rate = Decimal('0.20')
        discount = (order_total * discount_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        totals = {
        "Subtotal incl. VAT": '{:.2f}'.format(order_total)
        }

        totals["Total excl. VAT"] = '{:.2f}'.format(order_total - discount)
        totals["Total amount due"] = '{:.2f}'.format(order_total)


        try:
            pdf_buffer = generate_invoice(recipient_info, order_info, invoice_items, totals, order_detail)
            response = FileResponse(pdf_buffer, as_attachment=True, filename=f'Invoice #{order_reference}')
            messages.success(request, "Invoice Downloaded Successfully")
            return response

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('manage')
    
    return render(request, 'adminManage/create_invoice.html', ctx)


@require_POST
def update_order_status(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('orderId')
        status = data.get('status')
        
        try:
            order = Order.objects.get(id=order_id)
            if (status == 'sent' and order.sendable):
                order.status = status
                order.save()
                messages.success(request, 'Order status updated!')
                return JsonResponse({'message': 'Order status updated successfully'})
            else:
                messages.error(request, 'Order status cannot be updated at this time')
                return JsonResponse({'error': 'Order status cannot be updated at this time'}, status=400)
            
        except Order.DoesNotExist:
            messages.error(request, f'Order {order_id} not found')
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            messages.error(request, str(e))
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def send_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    cart = order.order_items.all()
    invoice_items = []

    user_profile = order.user.userprofile

    recipient_info = [
    user_profile.invoice_business,
    user_profile.invoice_address_line1,
    user_profile.invoice_address_line2,
    user_profile.invoice_address_line3,
    user_profile.invoice_postcode
    ]

    order_info = [
    "Order Reference: " + order_id,
    "Invoice Date: " + order.delivery_date.strftime('%d/%m/%Y'),
    "Payment Terms: 30 days"
    ]

    for item in cart:
        product = item.product.name
        quantity = item.quantity  
        price = '{:.2f}'.format(item.product.price)
        subtotal = '{:.2f}'.format(item.get_total())
        invoice_items.append({"description": product, "quantity": quantity, "price": price, "subtotal": subtotal},)

    totals = {
    "Subtotal incl. VAT": '{:.2f}'.format(order.order_total)
    }

    # Calculate the discount
    discount_rate = Decimal('0.20')
    discount = (order.order_total * discount_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Check if the user's profile is workspace
    if user_profile == "workspace":
        totals["Discount 20%"] = '{:.2f}'.format(discount)
        totals["Total excl. VAT"] = '{:.2f}'.format(order.order_total - discount)
        totals["Total amount due"] = '{:.2f}'.format(order.order_total - discount)
    else:
        totals["Total excl. VAT"] = '{:.2f}'.format(order.order_total - discount)
        totals["Total amount due"] = '{:.2f}'.format(order.order_total)

    try:
        invoice_buffer = generate_invoice(recipient_info, order_info, invoice_items, totals)
        pdf_filename = f"Invoice_{order_id}.pdf"
        with open(pdf_filename, 'wb') as tmp_file:
            tmp_file.write(invoice_buffer.getbuffer())
    except Exception as e:
        messages.error(request, "Failed to generate Invoice")
        return redirect('manage')

    email_content = render_to_string('email/email_body.html', {
    'order_id': order_id,
    'customer_name': user_profile.invoice_business,
    })

    subject = f"Invoice for Order #{order_id}"
    from_email = os.environ.get('SENDGRID_FROM_EMAIL')
    to_email = [user_profile.invoice_email]

    try:
        # Initialize SendGrid message
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=email_content
            )

        # Load PDF file
        with open(pdf_filename, 'rb') as f:
            attachment_data = f.read()
        encoded_attachment_data = base64.b64encode(attachment_data).decode()
        # Create attachment object
        attachment = Attachment(
            FileContent(encoded_attachment_data),
            FileName(pdf_filename),
            FileType('application/pdf'),
            Disposition('attachment')
        )

        # Add attachment to email message
        message.attachment = attachment

        # Initialize SendGrid client with API key
        sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)

        if response.status_code == 202:
            print("Response status code:", response.status_code)
            order.status = 'invoiced'
            order.save()
            os.remove(pdf_filename)  # Delete the temporary file after sending
            messages.success(request, f"Invoice sent for order {order_id}")
            return redirect('manage')
        else:
            os.remove(pdf_filename)
            messages.error(request, f"Failed to invoice order {order_id}")
            return redirect('manage')

    except Exception as e:
        os.remove(pdf_filename)
        messages.error(request, f"Failed to invoice order {order_id}")
        return redirect('manage')