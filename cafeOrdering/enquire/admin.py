from django.contrib import admin
from .models import Enquiry


class EnquiryAdmin(admin.ModelAdmin):
    display = ()


admin.site.register(Enquiry, EnquiryAdmin)


class EnquiryMeta:
    verbose_name = "Enquiry"  
    verbose_name_plural = "Enquiries"  


Enquiry._meta.verbose_name = "Enquiry"  
Enquiry._meta.verbose_name_plural = "Enquiries"  





