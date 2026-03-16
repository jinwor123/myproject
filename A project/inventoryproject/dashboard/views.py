from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Category,unit
from .forms import ProductForm,CategoryForm,unitForm

# Create your views here.
def index(request):
    return render(request,'dashboard/index.html')
def staff(request):
    return render (request,'dashboard/staff.html')
def product(request):
    
    products = Product.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('dashboard-product')
    else:  
        form = ProductForm()
    
    context = {
        'products': products,
        'form': form
    }
    return render(request, 'dashboard/product.html', context)

def add_category(request):
    """Display all categories"""
    categories = Category.objects.all()
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-category')
    else:  
        form = CategoryForm()
    
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'dashboard/category.html', context)

def delete_category(request, pk):
    """Delete a category"""
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('dashboard-category') 
    return render(request, 'dashboard/category.html', {'item': category})

def add_unit(request):
    """Display all units with inline add unit form"""
    units = unit.objects.all()
    
    if request.method == 'POST':
        form = unitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-unit')
    else:  
        form = unitForm()
    
    context = {
        'units': units,
        'form': form
    }
    return render(request, 'dashboard/unit.html', context)

def delete_unit(request, pk):
    """Delete a unit"""
    unit = unit.objects.get(pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('dashboard-unit') 
    return render(request, 'dashboard/unit.html', {'item': unit})
    
def order(request):
    return render (request,'dashboard/order.html')