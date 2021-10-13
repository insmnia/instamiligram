from .views import (
    CreateUserView,
    HomeUserProfileView,
    FollowUserView,
    UserProfileView
)
from django.urls import path

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("profile/", HomeUserProfileView.as_view(), name="profile"),
    path("follow/",FollowUserView.as_view(),name='follow'),
    path('uprofile/<str:username>',UserProfileView.as_view(),name="u-profile")
]
