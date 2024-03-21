from django.shortcuts import render

import os

def homepage(request):
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    ctx = {
        'google_maps_api_key': google_maps_api_key
    }
    return render(request, 'homepage/index.html', ctx)