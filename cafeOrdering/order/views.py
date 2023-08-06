from django.shortcuts import render

from products.models import Product


def order(request):
    products = Product.objects.all()

    ctx = {
    'products': products,
}


    return render(request, 'order/order.html', ctx)