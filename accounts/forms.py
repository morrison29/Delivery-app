from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomerSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_delivery_agent = False
        user.phone_number = self.cleaned_data.get('phone_number', '')
        if commit:
            user.save()
        return user
