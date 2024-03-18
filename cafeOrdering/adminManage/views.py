import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .pdf_generator import generate_invoice
from enquire.models import Enquiry
from decimal import Decimal, ROUND_HALF_UP
from order.models import Order
from products.models import InvoiceProduct

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def manage(request):
    enquiries = Enquiry.objects.all()
    orders = Order.objects.all()
    
    ctx = {
        'enquiries': enquiries,
        'orders': orders,
    }

    return render(request, 'adminManage/manage.html', ctx)


def filter_orders(request):
    status = request.GET.get('status')
    enquiries = Enquiry.objects.all()
    if status in dict(Order.ORDER_STATUS):
        orders = Order.objects.filter(status=status)
    else:
        orders = Order.objects.all()

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
    order_reference = ''.join(random.choices('0123456789', k=5))
    invoice_items = []

    ctx = {
        'products': products,
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

        generate_invoice(recipient_info, order_info, invoice_items, totals, order_detail)   

        return HttpResponse('Form submitted successfully.')

    return render(request, 'adminManage/create_invoice.html', ctx)


@require_POST
def update_order_status(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('orderId')
        status = data.get('status')
        
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            
            messages.success(request, 'Order status updated!')
            return JsonResponse({'message': 'Order status updated successfully'})
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
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
    print(discount)

    # Check if the user's profile is workspace
    if user_profile == "workspace":
        totals["Discount 20%"] = '{:.2f}'.format(discount)
        totals["Total excl. VAT"] = '{:.2f}'.format(order.order_total - discount)
        totals["Total amount due"] = '{:.2f}'.format(order.order_total - discount)
    else:
        totals["Total excl. VAT"] = '{:.2f}'.format(order.order_total - discount)
        totals["Total amount due"] = '{:.2f}'.format(order.order_total)

    print(totals)

    generate_invoice(recipient_info, order_info, invoice_items, totals)

    return HttpResponse("Invoice sent successfully")
    