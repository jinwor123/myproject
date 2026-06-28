from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Category, Unit, Product
from pos.models import POSSale, POSSaleItem


class POSFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Pet Food")
        self.unit = Unit.objects.create(name="Piece", symbol="pcs")
        self.product = Product.objects.create(
            name="Dog Food",
            category=self.category,
            unit=self.unit,
            quantity=20,
            cost_price=100,
            selling_price=150,
            sku="DOG001"
        )

    def test_search_product_api(self):
        response = self.client.get(reverse('pos-search'), {'q': 'Dog'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.json())

    def test_add_to_cart_api(self):
        response = self.client.post(
            reverse('pos-add'),
            {'product_id': self.product.id, 'quantity': 2}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['cart_count'], 1)

    def test_add_to_cart_insufficient_stock(self):
        response = self.client.post(
            reverse('pos-add'),
            {'product_id': self.product.id, 'quantity': 100}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'error')

    def test_update_cart_api(self):
        session = self.client.session
        session['pos_cart'] = {
            str(self.product.id): {
                'id': self.product.id,
                'name': self.product.name,
                'sku': self.product.sku,
                'price': float(self.product.selling_price),
                'quantity': 1,
                'total': float(self.product.selling_price),
                'unit': self.product.unit.symbol,
            }
        }
        session.save()

        response = self.client.post(
            reverse('pos-update'),
            {'product_id': self.product.id, 'quantity': 3}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')

    def test_remove_from_cart_api(self):
        session = self.client.session
        session['pos_cart'] = {
            str(self.product.id): {
                'id': self.product.id,
                'name': self.product.name,
                'sku': self.product.sku,
                'price': float(self.product.selling_price),
                'quantity': 1,
                'total': float(self.product.selling_price),
                'unit': self.product.unit.symbol,
            }
        }
        session.save()

        response = self.client.post(
            reverse('pos-remove'),
            {'product_id': self.product.id}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['cart_count'], 0)


    def test_checkout_success(self):
        session = self.client.session
        session['pos_cart'] = {
            str(self.product.id): {
                'id': self.product.id,
                'name': self.product.name,
                'sku': self.product.sku,
                'price': float(self.product.selling_price),
                'quantity': 2,
                'total': float(self.product.selling_price) * 2,
                'unit': self.product.unit.symbol,
            }
        }
        session.save()

        response = self.client.post(reverse('pos-checkout'))
        self.assertEqual(response.status_code, 302)

        sale = POSSale.objects.first()
        self.assertIsNotNone(sale)
        self.assertEqual(POSSaleItem.objects.count(), 1)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 18)

    def test_checkout_empty_cart(self):
        session = self.client.session
        session['pos_cart'] = {}
        session.save()

        response = self.client.post(reverse('pos-checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(POSSale.objects.count(), 0)


    def test_cancel_receipt(self):
        sale = POSSale.objects.create(
            sale_no="POS-123456",
            total_amount=300
        )
        POSSaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=2,
            unit_price=150,
            total_price=300
        )

        self.product.quantity = 18
        self.product.save()

        response = self.client.post(reverse('cancel-receipt', args=[sale.id]))
        self.assertEqual(response.status_code, 302)

        sale.refresh_from_db()
        self.assertTrue(sale.is_cancelled)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 20)