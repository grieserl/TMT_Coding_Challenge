from django.urls import reverse
from rest_framework.test import APITestCase

from interview.inventory.models import InventoryLanguage, InventoryType, Inventory


class TestInventoryAPI(APITestCase):
    def setUp(self):
        language = InventoryLanguage.objects.create(name="English")
        type = InventoryType.objects.create(name="Thriller")
        jurassic_park = Inventory.objects.create(
            name="Jurassic Park",
            language=language,
            type=type,
            metadata={}
        )
        the_lost_world = Inventory.objects.create(
            name="The Lost World: Jurassic Park",
            language=language,
            type=type,
            metadata = {}
        )
        jurassic_park.created_at = '2025-10-01'
        the_lost_world.created_at = '2025-10-02'
        jurassic_park.save()
        the_lost_world.save()

    def test_inventory_list_after_date(self):
        url = reverse("inventory-list-after-date", kwargs={"date": '2025-10-01'})
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2

        url = reverse("inventory-list-after-date", kwargs={"date": '2025-10-02'})
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1