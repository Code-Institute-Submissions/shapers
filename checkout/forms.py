from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Custom Form for the Order model"""

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'street_address1',
                  'street_address2', 'postcode', 'town_or_city',
                  'county', 'country']

    def __init__(self, *args, **kwargs):
        """
        Settings to init the form with, form field classes, placeholders, etc.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address',
            'street_address2': 'Housing Estate, Building, ...',
            'town_or_city': 'Town or City',
            'postcode': 'Postal Code',
            'county': 'County',
            'country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'form-control ' \
                                                       'col-12 col-md-6 ' \
                                                       'rounded-0'
            self.fields[field].label = False
