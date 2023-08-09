from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from order.models import Order


def sign_up(request):
    return render(request, 'users/signup.html') 

@login_required
def view_profile(request):
    user_profile = request.user.userprofile
    orders = Order.objects.filter(user=request.user) 
    
    ctx = {
        "orders": orders,
        'user_profile': user_profile,
    }

    return render(request, 'users/profile.html', ctx)
