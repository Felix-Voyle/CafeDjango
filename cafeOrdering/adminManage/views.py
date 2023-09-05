from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from enquire.models import Enquiry
from order.models import Order


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