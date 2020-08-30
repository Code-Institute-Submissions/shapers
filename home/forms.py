from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Custom Form for the Order model"""

    class Meta:
        model = Contact
        fields = ['email', 'full_name', 'message']

    def __init__(self, *args, **kwargs):
        """
        Settings to init the form with, form field classes, placeholders, etc.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'message': 'Your inquiry',
        }

        self.fields['email'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'form-control ' \
                                                       'col-12 col-md-8 ' \
                                                       'rounded-0'
            self.fields[field].label = False
