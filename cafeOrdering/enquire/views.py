from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import EnquiryForm

def enquire(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            form.save()

            messages.success(request, 'Enquiry sent successfully!')
            return redirect('/')
    else:
        form = EnquiryForm()
    return render(request, 'enquire/enquire.html', {'form': form})
