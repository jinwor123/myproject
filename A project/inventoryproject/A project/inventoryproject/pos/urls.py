from django.urls import path
from . import views


urlpatterns = [
    path('cashier/', views.cashier, name='cashier'),
    path('receipt/', views.receipt, name='receipt')
]