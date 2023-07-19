from django import forms
from .models import Product, Sale, Invoice, SaleItem, ShoppingCartItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name']

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = ShoppingCartItem
        fields = ['product', 'quantity']

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity_sold']

SaleItemFormSet = forms.inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['total_amount', 'invoice_number']

