from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from order.models import Order
from django.utils import timezone
from datetime import timedelta
from order.utils.helpers import redirect_based_on_role 

def sign_up(request):
    return render(request, 'users/signup.html')


def redirect_from_profile(request):
    return redirect_based_on_role(request)


@login_required
def my_orders(request):

    # Check if the user is staff or superuser
    if request.user.is_staff or request.user.is_superuser:
        # Redirect staff or superusers to the admin manage page
        return redirect('manage')  # Adjust the URL name as per your project setup

    user_profile = request.user.userprofile
    orders = Order.objects.filter(user=request.user).order_by('delivery_date')

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
        "orders": orders,
        'user_profile': user_profile,
    }

    return render(request, 'users/my_orders.html', ctx)

@login_required
def filter_my_orders(request):
    status = request.GET.get('status')

    today = timezone.now().date()

    if status == 'upcoming':
        orders = Order.objects.filter(delivery_date__gte=timezone.now()).order_by('delivery_date')
    elif status == "past":
        orders = Order.objects.filter(delivery_date__lt=today).order_by('-delivery_date')
    elif status == 'reported':
        orders = Order.objects.filter(problem_order=True).order_by('delivery_date')
    else:
        orders = Order.objects.order_by('delivery_date')

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
    }

    return render(request, 'users/my_orders.html', ctx)


@require_POST
def report_problem(request):
    # Extract data from the AJAX Post request
    order_id = request.POST.get('order_id')
    problem_description = request.POST.get('problem_description')

    if len(problem_description) > 200:
        messages.error(request, "Problem description can't be more than 200 characters")
        return HttpResponseRedirect(reverse('my_orders'))

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, f"Order {order_id} not found")
        return HttpResponseRedirect(reverse('my_orders'))
    
    # Update the order with the reported problem
    order.reported_problem = problem_description
    order.problem_order = True
    order.save()

    if order.reported_problem == problem_description:
        messages.success(request, 'Problem reported successfully!')
        return JsonResponse({'success': True, 'message': 'Problem reported successfully'})
    else:
        messages.error(request, "Failed to report problem.")
        return HttpResponseRedirect(reverse('my_orders'))
