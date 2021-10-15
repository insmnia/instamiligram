from .views import (
    CreateUserView,
    UserSettingsView,
    FollowUserView,
    UserProfileView
)
from django.urls import path

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("profile/<str:username>", UserProfileView.as_view(), name="profile"),
    path("follow/", FollowUserView.as_view(), name='follow'),
    path('settings/', UserSettingsView.as_view(), name="settings")
]
