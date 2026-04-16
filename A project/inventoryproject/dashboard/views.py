from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from .models import Product, Category, Unit
from .forms import ProductForm, CategoryForm, UnitForm
from pos.models import POSSaleItem

# Create your views here.
def index(request):
    return render(request,'dashboard/index.html')

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

def edit_product(request, pk):
    """Edit product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'is_edit': True
    }
    return render(request, 'dashboard/product.html', context)

def delete_product(request, pk):
    """Delete product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product.html', {'product': product})

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
    units = Unit.objects.all()
    
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-unit')
    else:  
        form = UnitForm()
    
    context = {
        'units': units,
        'form': form
    }
    return render(request, 'dashboard/unit.html', context)

def delete_unit(request, pk):
    """Delete a unit"""
    unit = Unit.objects.get(pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('dashboard-unit') 
    return render(request, 'dashboard/unit.html', {'item': unit})

def sales_summary(request):
    # สรุปยอดขายรายสินค้า (ทุกเวลา)
    summary = (
        POSSaleItem.objects
        .values('product__id', 'product__name', 'product__category__name')
        .annotate(
            total_qty=Sum('quantity'),
            total_amount=Sum('total_price'),
        )
        .order_by('-total_amount')
    )

    context = {'summary': summary}
    return render(request, 'dashboard/staff.html', context)
    
