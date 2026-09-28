from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import OrderCreateForm, OrderStatusForm
from .models import Order


@login_required
def dashboard(request):
    """
    Routes to the right view based on who's logged in:
    - delivery agent sees every order
    - customer sees only their own
    """
    if request.user.is_delivery_agent:
        orders = Order.objects.all()
        template = 'orders/agent_dashboard.html'
    else:
        orders = Order.objects.filter(customer=request.user)
        template = 'orders/customer_dashboard.html'
    return render(request, template, {'orders': orders})


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:dashboard')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, "Order placed! You'll be notified as it progresses.")
        return super().form_valid(form)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        # Customers can only open their own orders; the agent can open any.
        if self.request.user.is_delivery_agent:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)


@login_required
def update_status(request, pk):
    if not request.user.is_delivery_agent:
        messages.error(request, "Only the delivery agent can update order status.")
        return redirect('orders:dashboard')

    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.pk} updated to {order.get_status_display()}.")
            return redirect('orders:detail', pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'orders/update_status.html', {'form': form, 'order': order})
