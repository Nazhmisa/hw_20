from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"
        
    images = forms.FileField(
        widget=forms.FileInput(),
        required=False,
    )


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"