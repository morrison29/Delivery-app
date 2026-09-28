from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new/', views.OrderCreateView.as_view(), name='create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('<int:pk>/status/', views.update_status, name='update_status'),
]
