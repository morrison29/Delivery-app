from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomerSignUpForm


class SignUpView(CreateView):
    form_class = CustomerSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('orders:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
