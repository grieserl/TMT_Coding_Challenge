from django.urls import path

from interview.profiles.views import UserProfileListCreateView, UserProfileRetrieveUpdateView

urlpatterns = [
    path(
        "",
        UserProfileListCreateView.as_view(),
        name="user-profile-list-create",
    ),
    path(
        "<int:pk>",
        UserProfileRetrieveUpdateView.as_view(),
        name="user-profile-retrieve-update",
    )
]
