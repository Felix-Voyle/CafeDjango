from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def sign_up(request):
    return render(request, 'signup.html') 

@login_required
def view_profile(request):
    # Get the current user's profile
    user_profile = request.user.userprofile
    return render(request, 'profile.html', {'user_profile': user_profile})
