from .views import (
    CreateUserView,
    UserProfileView
)
from django.urls import path

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
