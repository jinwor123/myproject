from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm

# Create your views here.
def index(request):
    return render(request,'dashboard/index.html')
def staff(request):
    return render (request,'dashboard/staff.html')
def product(request):
    """Display all products"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'dashboard/product.html', context)
def add_product(request):
    """Add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product')
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'dashboard/product_form.html', context)
def order(request):
    return render (request,'dashboard/order.html')