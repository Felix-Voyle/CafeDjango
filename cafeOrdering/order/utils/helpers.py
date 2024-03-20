from django.shortcuts import redirect

def redirect_based_on_role(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('manage')
    else:
        return redirect('my_orders')