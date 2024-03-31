from django import forms
from crispy_forms.helper import FormHelper
from .models import Enquiry

def input_attrs(class_name, placeholder, autocomplete):
    return {
        'class': class_name,
        'placeholder': placeholder,
        'required': 'required',
        'autocomplete': autocomplete,
    }

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone_number', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        for field_name, field in self.fields.items():
            
            if field_name == 'phone_number':
                field.widget.input_type = 'tel'
            elif field_name == 'email':
                field.widget.input_type = 'email'
            else:
                field.widget.input_type = 'text'
            
            autocomplete = None
            if field_name == 'phone_number':
                autocomplete = 'tel'
            elif field_name == 'email':
                autocomplete = 'email'
            else:
                autocomplete = 'off'
            
            field.widget.attrs.update(input_attrs(f'{field_name}-input main-txt', field.label, autocomplete))