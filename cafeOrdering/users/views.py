from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from order.models import Order

def sign_up(request):
    return render(request, 'users/signup.html') 

@login_required
def view_profile(request):

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

    return render(request, 'users/profile.html', ctx)

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
