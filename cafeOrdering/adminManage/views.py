import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .pdf_generator import generate_invoice
from enquire.models import Enquiry
from order.models import Order

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def manage(request):
    enquiries = Enquiry.objects.all()
    orders = Order.objects.all()
    
    ctx = {
        'enquiries': enquiries,
        'orders': orders,
    }

    return render(request, 'adminManage/manage.html', ctx)



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

    generate_invoice(recipient_info, order_info, invoice_items)

    return HttpResponse("Invoice sent successfully")
    