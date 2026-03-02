from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name='dashboard-index'),
    path('staff/',views.staff,name='dashboard-staff'),
    path('product/', views.product, name='dashboard-product'),
    #path('product/add/', views.add_product, name='dashboard-add_product'),
    path('product/category/', views.add_category, name='dashboard-category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete-category'),
    path('order/',views.order,name='dashboard-order'),
]
