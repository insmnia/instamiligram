from .views import (
    CreateUserView,
    LoginView,
    UserSettingsView,
    FollowUserView,
    UserProfileView,
    UserFollowerView
)
from django.urls import path

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("profile/<str:username>", UserProfileView.as_view(), name="profile"),
    path("follow/", FollowUserView.as_view(), name='follow'),
    path('settings/', UserSettingsView.as_view(), name="settings"),
    path('login/',LoginView.as_view(),name="login"),
    path('followers',UserFollowerView.as_view(),name="followers")
]
