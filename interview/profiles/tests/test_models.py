from django.utils import timezone

from interview.profiles.models import UserProfile


def test_get_full_name():
    user_profile = UserProfile.objects.create(
        email="bboimler@cerritos.com",
        first_name="Bradward",
        last_name="Boimler",
        password="pass",
        date_joined=timezone.now(),
        last_login=timezone.now(),
        is_staff=True,
        is_active=True,
        is_admin=False,
    )
    assert (
        user_profile.get_full_name()
        == user_profile.first_name + " " + user_profile.last_name
    )


def test_get_username():
    user_profile = UserProfile.objects.create(
        email="bboimler@cerritos.com",
        first_name="Bradward",
        last_name="Boimler",
        password="pass",
        date_joined=timezone.now(),
        last_login=timezone.now(),
        is_staff=True,
        is_active=True,
        is_admin=False,
    )
    assert user_profile.get_username() == user_profile.email
