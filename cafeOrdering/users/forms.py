from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    is_workspace = forms.BooleanField(label='Workspace', required=False)
    address_line1 = forms.CharField(label='Address Line 1', max_length=100)
    address_line2 = forms.CharField(label='Address Line 2', max_length=100, required=False)
    address_line3 = forms.CharField(label='Address Line 3', max_length=100, required=False)
    postcode = forms.CharField(label='Postcode', max_length=10)
    invoice_business = forms.CharField(label='Business Name', max_length=100)
    invoice_address_line1 = forms.CharField(label='Invoice Address Line 1', max_length=100)
    invoice_address_line2 = forms.CharField(label='Invoice Address Line 2', max_length=100, required=False)
    invoice_address_line3 = forms.CharField(label='Invoice Address Line 3', max_length=100, required=False)
    invoice_postcode = forms.CharField(label='Invoice Postcode', max_length=100)
    invoice_email = forms.EmailField(label='Invoice Email')

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ('is_workspace', 'address_line1', 'address_line2', 'address_line3', 'postcode', 'invoice_business', 'invoice_address_line1', 'invoice_address_line2', 'invoice_address_line3', 'invoice_postcode', 'invoice_email',)