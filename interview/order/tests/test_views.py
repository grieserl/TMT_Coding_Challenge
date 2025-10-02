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

    def test_order_list_view_between_dates(self):
        # Should return order
        url = reverse('order-list-between-dates') + "?start_date=2025-01-01&embargo_date=2025-12-31"
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1

        # Filter out by start date
        url = reverse('order-list-between-dates') + "?start_date=2025-08-16&embargo_date=2025-12-31"
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 0

        # Filter out by embargo date
        url = reverse('order-list-between-dates') + "?start_date=2025-01-01&embargo_date=2025-09-14"
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 0