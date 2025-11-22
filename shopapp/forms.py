from django import forms

from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"
        
    images = forms.FileField(
        widget=forms.FileInput(attrs={"multiple": True}),
        required=False,
    )


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
