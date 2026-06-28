from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, DecimalField, ExpressionWrapper 
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import Product, Category, Unit
from .forms import ProductForm, CategoryForm, UnitForm
import json
from pos.models import POSSaleItem,POSSale
from django.utils import timezone

# Create your views here.
def _topnav_stats():
    active_products = Product.objects.filter(is_deleted=False)

    total_sales_amount = (
        POSSale.objects.filter(is_cancelled=False)
        .aggregate(total=Sum('total_amount'))
        .get('total') or 0
    )

    total_product_pieces = (
        active_products.aggregate(total=Sum('quantity')).get('total') or 0
    )

    total_orders = POSSale.objects.filter(is_cancelled=False).count()

    total_cost_stock = (
        active_products.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('cost_price') * F('quantity'),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                )
            )
        ).get('total') or 0
    )

    total_expected_profit_stock = (
        active_products.aggregate(
            total=Sum(
                ExpressionWrapper(
                    (F('selling_price') - F('cost_price')) * F('quantity'),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                )
            )
        ).get('total') or 0
    )

    return {
        "nav_total_sales_amount": total_sales_amount,
        "nav_total_product_pieces": total_product_pieces,
        "nav_total_orders": total_orders,
        "nav_total_cost_stock": total_cost_stock,
        "nav_total_expected_profit_stock": total_expected_profit_stock,
    }

    # แสดงหน้า Dashboard ในหน้าหลัก
def index(request):
    qs = (
        POSSaleItem.objects
        .filter(sale__is_cancelled=False)
        .values('product__category__name')
        .annotate(total_amount=Sum('total_price'))
        .order_by('-total_amount')
    )

    labels = [row['product__category__name'] or 'ไม่ระบุหมวดหมู่' for row in qs]
    amounts = [float(row['total_amount'] or 0) for row in qs]

    context = {
        'cat_labels': json.dumps(labels, ensure_ascii=False),
        'cat_amounts': json.dumps(amounts),
        **_topnav_stats(),
    }
    return render(request, 'dashboard/index.html', context)

# แสดงหน้าจัดการสินค้า
def product(request):
    products = Product.objects.all().order_by('is_deleted', 'quantity')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'form': form,
        **_topnav_stats(),
    }

    return render(request, 'dashboard/product.html', context)

# แก้ไขข้อมูลสินค้า
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
        'is_edit': True,
        **_topnav_stats(),
    }
    return render(request, 'dashboard/product.html', context)


def delete_product(request, pk):
    """Soft delete product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_deleted = True
        product.deleted_at = timezone.now()
        product.save(update_fields=["is_deleted", "deleted_at"])
        return redirect('dashboard-product')
    return render(request, 'dashboard/product.html', {'product': product})


def restore_product(request, pk):
    """Restore product and restore its category/unit if needed"""
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)

        # restore category ถ้าถูกลบอยู่
        if product.category and product.category.is_deleted:
            product.category.is_deleted = False
            product.category.deleted_at = None
            product.category.save(update_fields=["is_deleted", "deleted_at"])

        # restore unit ถ้ามีและถูกลบอยู่
        if product.unit and product.unit.is_deleted:
            product.unit.is_deleted = False
            product.unit.deleted_at = None
            product.unit.save(update_fields=["is_deleted", "deleted_at"])

        # restore product
        product.is_deleted = False
        product.deleted_at = None
        product.save(update_fields=["is_deleted", "deleted_at"])

    return redirect("dashboard-product")

#แสดงหน้าจัดการหมวดหมู่สินค้า
def add_category(request):
    """Display all categories"""
    categories = Category.objects.all().order_by('is_deleted', '-created_at')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-category')
    else:
        form = CategoryForm()

    context = {
        'categories': categories,
        'form': form,
        **_topnav_stats(),
    }
    return render(request, 'dashboard/category.html', context)


def delete_category(request, pk):
    """Soft delete category and soft delete all products in that category"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        now = timezone.now()

        category.is_deleted = True
        category.deleted_at = now
        category.save(update_fields=["is_deleted", "deleted_at"])

        Product.objects.filter(category=category, is_deleted=False).update(
            is_deleted=True,
            deleted_at=now
        )

        return redirect('dashboard-category')

    return render(request, 'dashboard/category.html', {'item': category})


def restore_category(request, pk):
    """Restore category and restore all products in that category"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.is_deleted = False
        category.deleted_at = None
        category.save(update_fields=["is_deleted", "deleted_at"])

        Product.objects.filter(category=category, is_deleted=True).update(
            is_deleted=False,
            deleted_at=None
        )

    return redirect('dashboard-category')

def edit_category(request, pk):
    """Edit category"""
    category = get_object_or_404(Category, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard-category')
    else:
        form = CategoryForm(instance=category)

    context = {
        'categories': categories,
        'form': form,
        'is_edit': True,
        'category_obj': category,
        **_topnav_stats(),
    }
    return render(request, 'dashboard/category.html', context)

def add_unit(request):
    """Display all units with inline add unit form"""
    units = Unit.objects.all().order_by('is_deleted', 'name')

    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-unit')
    else:
        form = UnitForm()

    context = {
        'units': units,
        'form': form,
        **_topnav_stats(),
    }
    return render(request, 'dashboard/unit.html', context)


def delete_unit(request, pk):
    """Soft delete unit"""
    unit = get_object_or_404(Unit, pk=pk)

    if request.method == 'POST':
        unit.is_deleted = True
        unit.deleted_at = timezone.now()
        unit.save(update_fields=["is_deleted", "deleted_at"])
        return redirect('dashboard-unit')

    return render(request, 'dashboard/unit.html', {'item': unit})


def restore_unit(request, pk):
    """Restore unit"""
    unit = get_object_or_404(Unit, pk=pk)

    if request.method == 'POST':
        unit.is_deleted = False
        unit.deleted_at = None
        unit.save(update_fields=["is_deleted", "deleted_at"])

    return redirect('dashboard-unit')

def edit_unit(request, pk):
    """Edit unit"""
    unit = get_object_or_404(Unit, pk=pk)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('dashboard-unit')
    else:
        form = UnitForm(instance=unit)

    context = {
        'units': Unit.objects.all(),
        'form': form,
        'is_edit': True,
        'edit_unit_obj': unit,
        **_topnav_stats(),
    }
    return render(request, 'dashboard/unit.html', context)

def sales_summary(request):
    profit_expr = ExpressionWrapper(
        (F('product__selling_price') - F('product__cost_price')) * F('quantity'),
        output_field=DecimalField(max_digits=14, decimal_places=2)
    )

    summary = (
        POSSaleItem.objects
        .filter(sale__is_cancelled=False)
        .values('product__id', 'product__name', 'product__category__name')
        .annotate(
            total_qty=Sum('quantity'),
            total_amount=Sum('total_price'),
            total_profit=Sum(profit_expr),
        )
        .order_by('-total_profit')
    )

    total_profit_all = (
        POSSaleItem.objects
        .filter(sale__is_cancelled=False)
        .aggregate(total=Sum(profit_expr))
        .get('total') or 0
    )

    total_sales_all = (
        POSSaleItem.objects
        .filter(sale__is_cancelled=False)
        .aggregate(total=Sum('total_price'))
        .get('total') or 0
    )

    context = {
        'summary': summary,
        'total_profit_all': total_profit_all,
        'total_sales_all': total_sales_all,
        **_topnav_stats(),
    }
    return render(request, 'dashboard/summary.html', context)