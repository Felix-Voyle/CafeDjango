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
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        name = self.fields['name'].widget
        email = self.fields['email'].widget
        message = self.fields['message'].widget
        
        name.attrs.update(input_attrs('text', 'name-input', 'Name', 'off'))
        email.attrs.update(input_attrs('email', 'email-input', 'Email', 'on'))
        message.attrs.update(input_attrs('text', 'msg-input', 'Message', 'off'))
        

