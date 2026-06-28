from django import forms
from .models import Product, Category, Unit

#แก้ไขข้อมูลสินค้า
class ProductForm(forms.ModelForm):
    #กำหนด model
    class Meta:
        model = Product
        fields = ['name', 'category', 'unit', 'sku', 'cost_price', 'selling_price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    #ตรวจสอบ SKU ซ้ำ
    def clean_sku(self):
        sku = (self.cleaned_data.get('sku') or '').strip()

        qs = Product.objects.filter(sku__iexact=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('This SKU already exists.')

        return sku
    #ราคาทุนต้องไม่ติดลบ
    def clean_cost_price(self):
        cost_price = self.cleaned_data.get('cost_price')
        if cost_price is not None and cost_price < 0:
            raise forms.ValidationError('Cost price cannot be negative.')
        return cost_price
    #
    def clean_selling_price(self):
        selling_price = self.cleaned_data.get('selling_price')
        if selling_price is not None and selling_price < 0:
            raise forms.ValidationError('Selling price cannot be negative.')
        return selling_price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity

   


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
        }

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError('Please enter a category name.')

        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('This category already exists.')

        return name


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'symbol']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unit name'
            }),
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter symbol'
            }),
        }

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError('Please enter a unit name.')
        return name

    def clean_symbol(self):
        symbol = (self.cleaned_data.get('symbol') or '').strip()
        if not symbol:
            raise forms.ValidationError('Please enter a unit symbol.')

        qs = Unit.objects.filter(symbol__iexact=symbol)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('This unit symbol already exists.')

        return symbol