from rest_framework.fields import CharField, DateTimeField, ImageField
from rest_framework.serializers import ModelSerializer

from interview.profiles.models import UserProfile


class UserProfileSerializer(ModelSerializer):
    password = CharField(write_only=True, required=False)
    date_joined = DateTimeField(read_only=True)
    last_login = DateTimeField(read_only=True)
    avatar = ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "is_staff",
            "is_superuser",
            "is_admin",
            "is_active",
            "avatar",
        ]

    def create(self, validated_data):
        # password must be set with instance.set_password()
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)

        instance.set_password(password)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        # Password must be set with instance.set_password()
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            validated_data.pop("password")

        # Only admins can update security-related fields
        if self.context["request"].user.is_admin:
            instance.is_staff = validated_data.get("is_staff", instance.is_staff)
            instance.is_superuser = validated_data.get(
                "is_superuser", instance.is_superuser
            )
            instance.is_admin = validated_data.get("is_admin", instance.is_admin)
            instance.is_active = validated_data.get("is_active", instance.is_active)

        instance.save()

        return instance