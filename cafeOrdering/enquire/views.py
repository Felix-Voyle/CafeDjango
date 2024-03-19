from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import EnquiryForm
import logging

logger = logging.getLogger(__name__)

def enquire(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                phone_number = form.cleaned_data['phone_number']
                subject = form.cleaned_data['subject']

                form.save()
                messages.success(request, 'Enquiry sent successfully!')
                return redirect('/')

            except Exception as e:
                logger.error("Error processing enquiry form: %s", str(e))
                messages.error(request, 'An error occurred while processing your enquiry. Please try again later.')
                return redirect('/')

        else:
            messages.error(request, 'The form you submitted was invalid')

    else:
        form = EnquiryForm()

    return render(request, 'enquire/enquire.html', {'form': form})
