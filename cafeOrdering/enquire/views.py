from django.shortcuts import render

def enquire(request):
    return render(request, 'enquire/enquire.html')
