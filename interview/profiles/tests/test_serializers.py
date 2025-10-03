from unittest.mock import MagicMock

import pytest
from django.contrib.auth import authenticate
from django.utils import timezone

from interview.profiles.models import UserProfile
from interview.profiles.serializers import UserProfileSerializer


@pytest.mark.django_db
def test_user_profile_serializer_update():
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

    admin_profile = UserProfile.objects.create(
        email="bmariner@cerritos.com",
        first_name="Beckett",
        last_name="Mariner",
        password="pass",
        date_joined=timezone.now(),
        last_login=timezone.now(),
        is_staff=True,
        is_active=True,
        is_admin=True,
    )


    mock_request = MagicMock()
    mock_request.user = user_profile
    mock_context = {"request": mock_request}
    data = {
        "email": "updated@exmaple.com",
        "first_name": "updated",
        "last_name": "updated",
        "password": "pass2",
        "is_staff": False,
        "is_active": False,
        "is_admin": True,
        "is_superuser": True,
    }

    serializer = UserProfileSerializer(
        instance=user_profile, data=data, context=mock_context
    )
    serializer.is_valid()
    profile = serializer.save()
    assert profile.email == data["email"]
    assert profile.first_name == data["first_name"]
    assert profile.last_name == data["last_name"]
    assert authenticate(username=data["email"], password=data["password"])
    # Non-admins cannot update security flags
    assert profile.is_staff
    assert profile.is_active
    assert not profile.is_admin
    assert not profile.is_superuser

    # retry as admin
    mock_request.user = admin_profile
    mock_context = {"request": mock_request}

    serializer = UserProfileSerializer(
        instance=user_profile, data=data, context=mock_context
    )
    serializer.is_valid()
    profile = serializer.save()
    assert not profile.is_staff
    assert not profile.is_active
    assert profile.is_admin
    assert profile.is_superuser
