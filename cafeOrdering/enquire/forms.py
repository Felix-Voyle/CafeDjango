from django import forms
from crispy_forms.helper import FormHelper
from .models import Enquiry

def input_attrs(type, class_name, placeholder, autocomplete):
    return({
        'type': type,
        'class': class_name,
        'placeholder': placeholder,
        'required': 'required',
        'autocomplete': autocomplete,
    })

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone_number', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        name = self.fields['name'].widget
        phone_number = self.fields['phone_number'].widget
        email = self.fields['email'].widget
        subject = self.fields['subject'].widget
        message = self.fields['message'].widget
        
        name.attrs.update(input_attrs('text', 'name-input main-txt', 'Name', 'off'))
        phone_number.attrs.update(input_attrs('tel', 'number-input main-txt', 'Phone Number', 'on'))
        email.attrs.update(input_attrs('email', 'email-input main-txt', 'Email', 'on'))
        subject.attrs.update(input_attrs('text', 'subject-input main-txt', 'Subject', 'off'))
        message.attrs.update(input_attrs('text', 'msg-input main-txt', 'Message', 'off'))

