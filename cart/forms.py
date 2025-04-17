from django import forms
from .models import Client

PRODUCT_QUANTITY_CHOICES = [(str(i), str(i)) for i in range(1, 21)]

# Form to Add Products to Cart
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

# Form to Collect Client Details
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contact_number', 'email', 'address', 'city', 'country', 'zip_code']
