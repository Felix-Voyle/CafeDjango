from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
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
    orders = Order.objects.filter(user=request.user) 
    
    ctx = {
        "orders": orders,
        'user_profile': user_profile,
    }

    return render(request, 'users/my_orders.html', ctx)


def filter_my_orders(request):
    status = request.GET.get('status')

    today = timezone.now().date()

    if status == 'upcoming':
        orders = Order.objects.filter(delivery_date__gte=timezone.now()).order_by('delivery_date')
    elif status == "past":
        orders = Order.objects.filter(delivery_date__lt=today).order_by('-delivery_date')
    elif status == 'reported':
        orders = Order.objects.filter(reported_problem=True)
    else:
        orders = Order.objects.order_by('delivery_date')

    ctx = {
        'orders': orders,
    }

    return render(request, 'users/my_orders.html', ctx)


@require_POST
def report_problem(request):
    # Extract data from the POST request
    order_id = request.POST.get('order_id')
    problem_description = request.POST.get('problem_description')

    # Fetch the order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
    
    # Update the order with the reported problem
    order.reported_problem = problem_description
    order.save()

    # Check if the reported problem was updated successfully
    if order.reported_problem == problem_description:
        messages.success(request, 'Problem reported successfully!')
        return JsonResponse({'success': True, 'message': 'Problem reported successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Failed to report problem'}, status=500)
