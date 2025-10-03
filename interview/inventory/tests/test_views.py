
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
            metadata={}
        )
        jurassic_park_iii = Inventory.objects.create(
            name="Jurassic Park III",
            language=language,
            type=type,
            metadata={}
        )

        jurassic_park.save()
        the_lost_world.save()
        jurassic_park_iii.save()



    def test_inventory_list_pagination(self):
        url = reverse("inventory-list")
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 3
        assert body[0]["name"] == "Jurassic Park"
        assert body[1]["name"] == "The Lost World: Jurassic Park"
        assert body[2]["name"] == "Jurassic Park III"

        url = reverse("inventory-list") + "?limit=2"
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2

        url = reverse("inventory-list") + "?offset=1"
        response = self.client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2
        assert body[0]["name"] == "The Lost World: Jurassic Park"

