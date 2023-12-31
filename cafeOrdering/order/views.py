from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Order, OrderItem
from products.models import Product, Category


def order(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    ctx = {
    'products': products,
    'categories': categories,
    }

    if request.method == 'POST':
        # Retrieve data from the form
        user = request.user
        address_line1 = request.POST['address_line1']
        address_line2 = request.POST.get('address_line2', '')
        address_line3 = request.POST.get('address_line3', '')
        postcode = request.POST['postcode']
        delivery_instructions = request.POST.get('delivery_instructions', '')
        delivery_date = request.POST.get('delivery_date', '')
        delivery_time = request.POST.get('delivery_time', '')


        order = Order.objects.create(
            user=user,
            address_line1=address_line1,
            address_line2=address_line2,
            address_line3=address_line3,
            postcode=postcode,
            delivery_instructions=delivery_instructions,
            delivery_date=delivery_date,
            delivery_time=delivery_time
        )

        order.save()


        product_ids = request.POST.getlist('confirmed-product')
        quantities = request.POST.getlist('confirmed-qty')


        for product_id, quantity in zip(product_ids, quantities):
            if int(quantity) > 0:
                product = Product.objects.get(pk=product_id)
                quantity = int(quantity)

                OrderItem.objects.create(order=order, product=product, quantity=quantity)

        order.update_total()
        messages.success(request, 'Order placed successfully!')
        return redirect('/')

    else:
        products = Product.objects.all()


    return render(request, 'order/order.html', ctx)


def product_search(request):
    keywords = request.GET.get('keywords', '')
    category_name = request.GET.get('category', '')

    products = Product.objects.all()

    if keywords:
        products = products.filter(name__icontains=keywords) | products.filter(description__icontains=keywords)

    if category_name:
        products = products.filter(category__name=category_name)

    categories = Category.objects.all()

    ctx = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'order/order.html', ctx)