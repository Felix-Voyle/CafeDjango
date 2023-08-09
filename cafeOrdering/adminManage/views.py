from django.shortcuts import render

from enquire.models import Enquiry
from order.models import Order


def manage(request):
    enquiries = Enquiry.objects.all()
    orders = Order.objects.all()
    

    ctx = {
    'enquiries': enquiries,
    'orders': orders,
    }

    print(ctx)


    return render(request, 'adminManage/manage.html', ctx)
