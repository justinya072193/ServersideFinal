from django import forms

class NewAddressForm(forms.Form):
    addressLine1 = forms.CharField(label='Address Line 1', max_length=250, required=True)
    addressLine2 = forms.CharField(label='Address Line 2', max_length=250)
    city = forms.CharField(label='City', max_length=250, required=True)
    state = forms.CharField(label='State', max_length=30, required=True)
    postalCode = forms.CharField(label='Postal Code', max_length=10, required=True)
    country = forms.CharField(label='Country', max_length=250, required=False)