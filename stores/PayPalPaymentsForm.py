# yourapp/forms.py
from django import forms
from .models import OrderProduct

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['order_by', 'address', 'phone', 'email', 'amount', 'total']
        widgets = {
            'order_by': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'address': forms.TextInput(attrs={'placeholder': 'Shipping address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'amount': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Quantity'}),
            'total': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Total price'}),
        }
