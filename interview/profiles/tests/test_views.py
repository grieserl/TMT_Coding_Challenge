
from django.urls import reverse

from rest_framework.test import APITestCase

from interview.profiles.models import UserProfile


class TestUserProfileAPI(APITestCase):
    def setUp(self):
        # base user (non-admin)
        self.user = UserProfile.objects.create(
            email="user@example.com",
            first_name="User",
            last_name="One",
            is_admin=False,
            is_active=True,
        )
        self.user.set_password("pass")
        self.user.save()

        # another user
        self.other = UserProfile.objects.create(
            email="other@example.com",
            first_name="Other",
            last_name="Two",
            is_admin=False,
            is_active=True,
        )
        self.other.set_password("pass")
        self.other.save()

        # admin user
        self.admin = UserProfile.objects.create(
            email="admin@example.com",
            first_name="Admin",
            last_name="Root",
            is_admin=True,
            is_staff=True,
            is_active=True,
        )
        self.admin.set_password("pass")
        self.admin.save()

    def test_create_user(self):
        data = {
            "email": "bboimler@cerritos.com",
            "password": "pass",
            "first_name": "Bradward",
            "last_name": "Boimler",
            "date_joined": "2020-07-22",
            "last_login": "2020-07-23",
            "is_staff": True,
            "is_active": True,
            "is_admin": True,
            "is_superuser": False,
        }
        url = reverse("user-profile-list-create")
        response = self.client.post(url, data)
        assert response.status_code == 403  # Not yet authenticated

        self.client.login(username=self.other.email, password="pass")
        response = self.client.post(url, data)
        assert response.status_code == 403  # Not an admin

        self.client.login(username=self.admin.email, password="pass")
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_list_users(self):
        url = reverse("user-profile-list-create")
        response = self.client.get(url)

        assert response.status_code == 403  # Not yet authenticated

        self.client.login(username=self.user.email, password="pass")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1  # Non-admin should only return themselves
        assert response.json()[0]["id"] == self.user.id

        self.client.login(username=self.admin.email, password="pass")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 3  # Admin should return all users

    def test_update_users(self):
        data = {
            "email": "bboimler@cerritos.com",
            "password": "pass",
            "first_name": "Updated",
            "last_name": "Boimler",
            "date_joined": "2020-07-22",
            "last_login": "2020-07-23",
            "is_staff": True,
            "is_active": True,
            "is_admin": True,
            "is_superuser": False,
        }

        self.client.login(username=self.user.email, password="pass")
        url = reverse("user-profile-retrieve-update", kwargs={"pk": self.other.id})
        response = self.client.patch(url, data)
        assert response.status_code == 404  # Non-admin can only update themselves

        url = reverse("user-profile-retrieve-update", kwargs={"pk": self.user.id})
        response = self.client.patch(url, data)
        assert response.status_code == 200  # Non-admin can update themselves

        self.client.login(username=self.admin.email, password="pass")
        data["email"] = "bmariner@cerritos.com"
        url = reverse("user-profile-retrieve-update", kwargs={"pk": self.other.id})
        response = self.client.patch(url, data)
        assert response.status_code == 200  # Admin can update anyone
