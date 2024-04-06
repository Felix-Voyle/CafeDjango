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
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import FileResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# Local application imports
from .pdf_generator import generate_invoice
from enquire.models import Enquiry
from order.models import Order, ServiceItem
from products.models import InvoiceProduct
from .models import ManageInvoice


def get_enquiries(request, viewed=None):
    try:
        enquiries = Enquiry.objects.all()
        if viewed is not None:
            enquiries = enquiries.filter(viewed=viewed)
        return enquiries
    except Exception as e:
        messages.error(request, "Failed to fetch Enquiries")
        return None


def get_invoices(request):
    try:
        return ManageInvoice.objects.all()
    except Exception as e:
        messages.error(request, "Failed to fetch Invoices")
        return None

def return_referer(request, redirect_url):
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(redirect_url)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def manage(request):
    enquiries = get_enquiries(request)
    invoices = get_invoices(request)
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
        'invoices': invoices,
    }

    return render(request, 'adminManage/manage.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def filter_orders(request):
    status = request.GET.get('status')
    enquiries = get_enquiries(request)
    invoices = get_invoices(request)
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
        'invoices': invoices,
    }

    return render(request, 'adminManage/manage.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def enquiries(request):
    unread_enquiries = get_enquiries(request, viewed=False)
    viewed_enquiries = get_enquiries(request, viewed=True)
    invoices = get_invoices(request)
    
    ctx = {
        'unread_enquiries': unread_enquiries,
        'viewed_enquiries': viewed_enquiries,
        'invoices': invoices,
    }

    return render(request, 'adminManage/enquiries.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def enquiry(request, enquiry_id):
    enquiries = get_enquiries(request)
    invoices = get_invoices(request)

    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    enquiry.viewed = True
    enquiry.save()
    ctx = {
        'enquiry': enquiry,
        'enquiries': enquiries,
        'invoices': invoices,
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
    enquiries = get_enquiries(request)
    invoices = get_invoices(request)

    order_reference = ''.join(random.choices('0123456789', k=5))
    invoice_items = []

    ctx = {
        'products': products,
        'enquiries': enquiries,
        'invoices': invoices,
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



@user_passes_test(lambda user: user.is_superuser or user.is_staff)
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


@transaction.atomic
def add_services(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        order_detail = request.POST.get('invoiceDetails')
        service_descriptions = request.POST.getlist('serviceDescription')
        service_prices = request.POST.getlist('servicePrice')
        
        try:
            if len(order_detail) < 6 or len(order_detail) > 100:
                raise ValueError("Order detail should be between 5 and 100 characters long")
            
            order.order_detail = order_detail
            order.save()
            
            for service_description, service_price in zip(service_descriptions, service_prices):
                if not service_description or not service_price:
                    raise ValueError("Service description and price are required for all services")
                
                if len(service_description) < 3 or len(service_description) > 50:
                    raise ValueError("Service description should be between 3 and 50 characters long")
                
                service_price = float(service_price)
                if not 0 <= service_price < 10000:
                    raise ValueError("Invalid price format. Price should be up to 7 digits including 2 decimal places")
                
                ServiceItem.objects.create(order=order, service=service_description, price=service_price)
            
            messages.success(request, "Successfully added final order detail")
            return return_referer(request, 'manage')
        
        except ValueError as e:
            messages.error(request, str(e))
            return return_referer(request, 'manage')
    
    messages.error(request, "This URL only accepts POST requests")
    return return_referer(request, 'manage')


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def send_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    cart = order.order_items.all()
    services = order.service_items.all()
    print(services)
    invoice_items = []

    user_profile = order.user.userprofile
    order_detail = order.order_detail

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

    total_service_price = 0

    for item in cart:
        product = item.product.name
        quantity = item.quantity  
        price = '{:.2f}'.format(item.product.price)
        subtotal = '{:.2f}'.format(item.get_total())
        invoice_items.append({"description": product, "quantity": quantity, "price": price, "subtotal": subtotal},)
    for service_item in services:
        service = service_item.service
        price = service_item.price 
        total_service_price += price 
        invoice_items.append({"description": service, "quantity": "", "price": price, "subtotal": price},)

    total_incl_vat = order.order_total + total_service_price

    total_incl_vat_formatted = '{:.2f}'.format(total_incl_vat)

    totals = {
    "Subtotal incl. VAT": total_incl_vat_formatted
    }

    # Calculate the discount
    discount_rate = Decimal('0.20')
    discount = (total_incl_vat * discount_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_excl_vat_formatted = '{:.2f}'.format(total_incl_vat - discount)

    # Check if the user's profile is workspace
    if user_profile == "workspace":
        totals["Discount 20%"] = '{:.2f}'.format(discount)
        totals["Total excl. VAT"] = total_excl_vat_formatted
        totals["Total amount due"] = total_excl_vat_formatted
    else:
        totals["Total excl. VAT"] = total_excl_vat_formatted
        totals["Total amount due"] = total_incl_vat_formatted

    try:
        invoice_buffer = generate_invoice(recipient_info, order_info, invoice_items, totals, order_detail)
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
            order.status = 'invoiced'
            order.save()
            os.remove(pdf_filename)
            try:
                ManageInvoice.objects.create(
                invoice_reference=order.order_id,
                invoice_date=order.delivery_date,
                invoice_sent_date=timezone.now().date(),
                invoice_total=order.order_total
            )   
                messages.success(request, f"Invoice sent for order {order_id}")
                return redirect('manage')
            except Exception as e:
                print(f"error, {e}")
                messages.error(request, "Invoice sent but failed to create manage invoice instance")
                return redirect('manage')
        else:
            os.remove(pdf_filename)
            messages.error(request, f"Failed to send email invoice for order {order_id}")
            return redirect('manage')

    except Exception as e:
        os.remove(pdf_filename)
        messages.error(request, f"Failed to invoice order {order_id}")
        return redirect('manage')


def due_invoices_count_value(request):
    try:
        due_invoices_count = ManageInvoice.objects.filter(invoice_paid=False, invoice_date__lte=timezone.now() - timezone.timedelta(days=30)).count()
        return due_invoices_count
    except Exception as e:
        messages.error(request, "Failed to fetch due invoices count")
        due_invoices_count = 0
        return due_invoices_count


def manage_invoices(request):
    try:
        invoices = ManageInvoice.objects.all().order_by('invoice_date')
        invoices = [invoice for invoice in invoices if invoice.is_due() and not invoice.invoice_paid]

        items_per_page = 20

        paginator = Paginator(invoices, items_per_page) 
        page = request.GET.get('page')
        try:
            invoices = paginator.page(page)
        except PageNotAnInteger:
            invoices = paginator.page(1)
        except EmptyPage:
            invoices = paginator.page(paginator.num_pages)
    except Exception as e:
        messages.error(request, "Failed to fetch Invoices")
        return redirect('manage')
    
    due_invoices_count = due_invoices_count_value(request)
    enquiries = get_enquiries(request)

    ctx = {
        'invoices': invoices,
        'due_invoices_count': due_invoices_count,
        'enquiries': enquiries,
        'paginator': paginator,
    }

    return render(request, 'adminManage/manage_invoices.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def filter_invoices(request):
    status = request.GET.get('status')

    try:
        invoices = ManageInvoice.objects.all().order_by('invoice_date')
        invoices = [invoice for invoice in invoices if invoice.is_due() and not invoice.invoice_paid]
    except Exception as e:
        messages.error(request, "Failed to fetch Invoices")
        return_referer(request, 'manage')

    try:
        if status == "all":
            invoices = ManageInvoice.objects.all().order_by('-invoice_date')
        elif status == "paid":
            invoices = ManageInvoice.objects.all().filter(invoice_paid=True).order_by('-invoice_date')
        elif status == "unpaid":
            invoices = ManageInvoice.objects.all().filter(invoice_paid=False).order_by('invoice_date')
    except ObjectDoesNotExist:
        messages.error(request, 'Failed to retrieve invoices: Object does not exist.')
        return_referer(request, 'manage_invoices')
    except ValidationError as e:
        messages.error(request, f'Failed to filter invoices: {e.message}.')
        return_referer(request, 'manage_invoices')
    
    items_per_page = 20

    paginator = Paginator(invoices, items_per_page) 
    page = request.GET.get('page')

    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)

    due_invoices_count = due_invoices_count_value(request)
    enquiries = get_enquiries(request)

    ctx = {
        'invoices': invoices,
        'due_invoices_count': due_invoices_count,
        'enquiries': enquiries,
        'paginator': paginator,
    }

    return render(request, 'adminManage/manage_invoices.html', ctx)


@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def mark_invoice_paid(request, invoice_reference):
    try:
        if invoice_reference:
            invoice = ManageInvoice.objects.get(invoice_reference=invoice_reference)
            invoice.invoice_paid = True
            invoice.save()
            messages.success(request, "Marked invoice as paid")
    except ObjectDoesNotExist:
        messages.error(request, f'Failed to find invoice {invoice_reference}.')
        return redirect('manage_invoices')
    except ValidationError as e:
        messages.error(request, f'Failed to mark invoice {invoice_reference} as paid: {e.message}.')
        return redirect('manage_invoices')
    
    return_referer(request, 'manage_invoices')