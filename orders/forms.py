from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['description', 'pickup_location', 'delivery_address']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': "What do you need picked up?"}),
            'pickup_location': forms.TextInput(attrs={'placeholder': "Where should it be picked up from? (optional)"}),
            'delivery_address': forms.TextInput(attrs={'placeholder': "Where should it be delivered?"}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'fee']
