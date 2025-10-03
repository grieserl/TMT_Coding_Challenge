from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from interview.profiles.models import UserProfile
from interview.profiles.serializers import UserProfileSerializer


# ASSUMPTIONS:
# Only Admins can create profiles
# Non-admins can only update or retrieve their own profile

class UserProfileListCreateView(ListCreateAPIView):
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        if (not self.request.user.is_authenticated) or not self.request.user.is_admin:
            raise PermissionDenied
        else:
            super().perform_create(serializer)



class UserProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.filter(pk=self.request.user.id)
