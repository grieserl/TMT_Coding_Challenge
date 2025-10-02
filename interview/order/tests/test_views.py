from django.urls import reverse

from rest_framework.test import APITestCase

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order

class TestOrderAPI(APITestCase):
    def setUp(self):
        language = InventoryLanguage.objects.create(name="English")
        type = InventoryType.objects.create(name="Thriller")
        jurassic_park = Inventory.objects.create(
            name="Jurassic Park",
            language=language,
            type=type,
            metadata={},
        )
        self.order = Order.objects.create(
            inventory=jurassic_park,
            start_date='2025-01-01',
            embargo_date='2025-12-31',
            is_active=True
        )
        self.order.save()

    def test_deactivate_order_view(self):
        url=reverse('order-deactivate', kwargs={'id': self.order.id})
        response=self.client.post(url)
        assert response.status_code==204
        self.order = Order.objects.get(id=self.order.id)
        assert not self.order.is_active