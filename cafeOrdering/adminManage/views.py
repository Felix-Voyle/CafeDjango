from django.shortcuts import render

from enquire.models import Enquiry


def manage(request):
    enquiries = Enquiry.objects.all()

    ctx = {
    'enquiries': enquiries,
}


    return render(request, 'adminManage/manage.html', ctx)
