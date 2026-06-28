from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse

from dashboard.forms import ProductForm
from dashboard.models import Category, Unit, Product
from dashboard.views import _topnav_stats


class ProductModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Pet Food")
        self.unit = Unit.objects.create(name="Piece", symbol="pcs")

    def test_profit_per_unit(self):
        product = Product.objects.create(
            name="Dog Food",
            category=self.category,
            unit=self.unit,
            quantity=10,
            cost_price=100,
            selling_price=150,
            sku="DOG001"
        )
        self.assertEqual(product.profit_per_unit, 50)

    def test_profit_margin(self):
        product = Product.objects.create(
            name="Cat Food",
            category=self.category,
            unit=self.unit,
            quantity=5,
            cost_price=80,
            selling_price=120,
            sku="CAT001"
        )
        self.assertEqual(float(product.profit_margin), 50.0)

class SoftDeleteCategoryUnitProductTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(name="Drink")
        self.unit = Unit.objects.create(name="Bottle", symbol="BTL")

        self.product1 = Product.objects.create(
            name="Cola",
            category=self.category,
            unit=self.unit,
            quantity=10,
            cost_price=10,
            selling_price=15,
            sku="COLA001"
        )
        self.product2 = Product.objects.create(
            name="Soda",
            category=self.category,
            unit=self.unit,
            quantity=20,
            cost_price=12,
            selling_price=18,
            sku="SODA001"
        )

    def test_delete_product_soft_delete(self):
        response = self.client.post(reverse('dashboard-delete-product', args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)

        self.product1.refresh_from_db()
        self.assertTrue(self.product1.is_deleted)
        self.assertIsNotNone(self.product1.deleted_at)

    def test_restore_product_only(self):
        self.product1.is_deleted = True
        self.product1.save()

        response = self.client.post(reverse('dashboard-restore-product', args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)

        self.product1.refresh_from_db()
        self.assertFalse(self.product1.is_deleted)
        self.assertIsNone(self.product1.deleted_at)

    def test_delete_category_soft_delete_category_and_products(self):
        response = self.client.post(reverse('delete-category', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)

        self.category.refresh_from_db()
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertTrue(self.category.is_deleted)
        self.assertIsNotNone(self.category.deleted_at)

        self.assertTrue(self.product1.is_deleted)
        self.assertTrue(self.product2.is_deleted)
        self.assertIsNotNone(self.product1.deleted_at)
        self.assertIsNotNone(self.product2.deleted_at)

    def test_restore_category_restore_products_in_same_category(self):
        self.category.is_deleted = True
        self.category.deleted_at = None
        self.category.save()

        self.product1.is_deleted = True
        self.product1.deleted_at = None
        self.product1.save()

        self.product2.is_deleted = True
        self.product2.deleted_at = None
        self.product2.save()

        response = self.client.post(reverse('restore-category', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)

        self.category.refresh_from_db()
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertFalse(self.category.is_deleted)
        self.assertIsNone(self.category.deleted_at)

        self.assertFalse(self.product1.is_deleted)
        self.assertFalse(self.product2.is_deleted)
        self.assertIsNone(self.product1.deleted_at)
        self.assertIsNone(self.product2.deleted_at)



    def test_restore_product_also_restores_deleted_category_and_unit(self):
        self.category.is_deleted = True
        self.category.deleted_at = None
        self.category.save()

        self.unit.is_deleted = True
        self.unit.deleted_at = None
        self.unit.save()

        self.product1.is_deleted = True
        self.product1.deleted_at = None
        self.product1.save()

        response = self.client.post(reverse('dashboard-restore-product', args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)

        self.category.refresh_from_db()
        self.unit.refresh_from_db()
        self.product1.refresh_from_db()

        self.assertFalse(self.category.is_deleted)
        self.assertIsNone(self.category.deleted_at)

        self.assertFalse(self.unit.is_deleted)
        self.assertIsNone(self.unit.deleted_at)

        self.assertFalse(self.product1.is_deleted)
        self.assertIsNone(self.product1.deleted_at)

    def test_product_form_hides_deleted_category_and_unit(self):
        deleted_category = Category.objects.create(
            name="Deleted Category",
            is_deleted=True
        )
        deleted_unit = Unit.objects.create(
            name="Deleted Unit",
            symbol="DEL",
            is_deleted=True
        )

        form = ProductForm()

        self.assertIn(self.category, form.fields['category'].queryset)
        self.assertNotIn(deleted_category, form.fields['category'].queryset)

        self.assertIn(self.unit, form.fields['unit'].queryset)
        self.assertNotIn(deleted_unit, form.fields['unit'].queryset)

    def test_topnav_stats_excludes_soft_deleted_products(self):
        self.product2.is_deleted = True
        self.product2.deleted_at = None
        self.product2.save()

        stats = _topnav_stats()

        self.assertEqual(stats['nav_total_product_pieces'], 10)
        self.assertEqual(stats['nav_total_cost_stock'], Decimal('100'))
        self.assertEqual(stats['nav_total_expected_profit_stock'], Decimal('50'))
