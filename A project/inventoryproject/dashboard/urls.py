from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('staff/',views.staff,name='staff'),
    path('product/', views.product, name='product'),
    path('product/add/', views.add_product, name='add-product'),
    path('order/',views.order,name='order'),
]
