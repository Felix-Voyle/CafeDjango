from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_workspace = models.BooleanField('Workspace', default=False)
    address_line1 = models.CharField('Address Line 1', max_length=100)
    address_line2 = models.CharField('Address Line 2', max_length=100, blank=True, null=True)
    address_line3 = models.CharField('Address Line 3', max_length=100, blank=True, null=True)
    postcode = models.CharField('Postcode', max_length=10)
    invoice_business = models.CharField('Business Name', max_length=100)
    invoice_address_line1 = models.CharField('Invoice Address Line 1', max_length=100)
    invoice_address_line2 = models.CharField('Invoice Address Line 2', max_length=100, blank=True, null=True)
    invoice_address_line3 = models.CharField('Invoice Address Line 3', max_length=100, blank=True, null=True)
    invoice_postcode = models.CharField('Invoice Postcode', max_length=100)
    invoice_email = models.EmailField()


    def __str__(self):
        return self.user.username
    
