from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
import logging
import json
from .models import Order, OrderItem
from products.models import Product, Category
from .utils.helpers import redirect_based_on_role
from .forms import validate_order_form_data

logger = logging.getLogger(__name__)


@transaction.atomic
def order(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    if hasattr(request.user, 'userprofile'):
        user_profile = request.user.userprofile
        initial_data = {
            'address_line1': user_profile.address_line1,
            'address_line2': user_profile.address_line2,
            'address_line3': user_profile.address_line3,
            'postcode': user_profile.postcode,
        }
    else:
        initial_data = {}

    ctx = {
        'products': products,
        'categories': categories,
        'initial_data': initial_data,
    }

    if request.method == 'POST':
        errors = validate_order_form_data(request.POST)
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return redirect('order')
        user = request.user
        address_line1 = request.POST['address_line1']
        address_line2 = request.POST.get('address_line2', '')
        address_line3 = request.POST.get('address_line3', '')
        postcode = request.POST['postcode']
        delivery_instructions = request.POST.get('delivery_instructions', '')
        delivery_date = request.POST.get('delivery_date')
        delivery_time = request.POST.get('delivery_time')

        order = Order(
            user=user,
            address_line1=address_line1,
            address_line2=address_line2,
            address_line3=address_line3,
            postcode=postcode,
            delivery_instructions=delivery_instructions,
            delivery_date=delivery_date,
            delivery_time=delivery_time
        )

        try:
            order.full_clean()  # Validate the order fields
            order.save()
        except ValidationError as e:
            messages.error(request, "Invalid order data. Please check your input.")
            logger.error("Validation error in order creation: %s", e)
            return redirect_based_on_role(request)
        except IntegrityError as e:
            messages.error(request, "Couldn't save order due to database error.")
            logger.error("Database error in order creation: %s", e)
            return redirect_based_on_role(request)

        product_ids = request.POST.getlist('confirmed-product')
        quantities = request.POST.getlist('confirmed-qty')

        try:
            for product_id, quantity in zip(product_ids, quantities):
                if int(quantity) > 0:
                    product = Product.objects.get(pk=product_id)
                    quantity = int(quantity)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

            order.update_total()
            messages.success(request, 'Order placed successfully!')
            return redirect_based_on_role(request)
        except Exception as e:
            messages.error(request, "Failed to place order.")
            logger.error("Error in order placement: %s", e)
            return redirect_based_on_role(request)

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
        'validation_errors': False
    }

    return render(request, 'order/order.html', ctx)


@transaction.atomic
def edit_order(request, order_id):
    try:
        order = get_object_or_404(Order, order_id=order_id)
    except Exception as e:
        messages.error(request, f"Could not find Order {order_id}")
        logger.error("Error finding Order %s: %s", order_id, e)
        return redirect('order')

    if request.method == 'POST':
        errors = validate_order_form_data(request.POST)
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return redirect('edit_order', order_id=order_id)
        try:
            # Retrieve data from the form
            address_line1 = request.POST.get('address_line1', order.address_line1)
            address_line2 = request.POST.get('address_line2', '')
            address_line3 = request.POST.get('address_line3', '')
            postcode = request.POST.get('postcode', order.postcode)
            delivery_instructions = request.POST.get('delivery_instructions', '')
            delivery_date = request.POST.get('delivery_date', order.delivery_date)
            delivery_time = request.POST.get('delivery_time', order.delivery_time)

            # Update order fields
            order.address_line1 = address_line1
            order.address_line2 = address_line2
            order.address_line3 = address_line3
            order.postcode = postcode
            order.delivery_instructions = delivery_instructions
            order.delivery_date = delivery_date
            order.delivery_time = delivery_time

            if request.user.is_superuser or request.user.is_staff:
                resolution_message = request.POST.get('resolution_message', '')
                if resolution_message and len(resolution_message) > 200:
                    errors['resolution_message'] = "Resolution message can't be longer than 200 characters."
                order.resolve_problem(resolution_message=resolution_message)

            # Update or delete existing order items
            if set(order.order_items.values_list('id', flat=True)) != set(request.POST.getlist('confirmed-product')):
                order.order_items.all().delete()

            # Create new order items
            for product_id, quantity in zip(request.POST.getlist('confirmed-product'), request.POST.getlist('confirmed-qty')):
                if int(quantity) > 0:
                    product = Product.objects.get(pk=product_id)
                    quantity = int(quantity)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)
            
            order.full_clean()
            order.update_total()
            order.save()
            messages.success(request, 'Order updated successfully!')
            return redirect_based_on_role(request)
        except Exception as e:
            messages.error(request, 'Failed to update order')
            logger.error("Error updating order %s: %s", order_id, e)
            return redirect_based_on_role(request)

    # If it's a GET request, populate the context with necessary data
    products = Product.objects.all()
    quantities = {item.product_id: item.quantity for item in order.order_items.all()}
    cart_data = {}
    for item in order.order_items.all():
        cart_data[item.product_id] = {
            'name': item.product.name,
            'quantity': item.quantity,
            'price': str(item.product.price),
        }

    initial_data = {
        'address_line1': order.address_line1,
        'address_line2': order.address_line2,
        'address_line3': order.address_line3,
        'postcode': order.postcode,
        'delivery_instructions': order.delivery_instructions,
        'delivery_date': order.delivery_date,
        'delivery_time': order.delivery_time,
    }

    ctx = {
        'order': order,
        'products': products,
        'quantities': quantities,
        'cart_data': json.dumps(cart_data),
        'initial_data': initial_data,
    }
    
    return render(request, 'order/edit_order.html', ctx)


def delete_order(request, order_id):
    try:
        order = get_object_or_404(Order, order_id=order_id)
    except:
        messages.error(request, f"Couldn't find order {order_id}")
        logger.error("Couldn't locate order %s: %s", order_id, e)
        return redirect_based_on_role(request)

    try:
        order.delete()
        messages.success(request, f"Order {order_id} cacncelled successfully")
        return redirect_based_on_role(request)
    except Exception as e:
        messages.error(request, f"An error occurred while deleting order {order_id}")
        logger.error("Couldn't delete order %s: %s", order_id, e)
        return redirect_based_on_role(request)