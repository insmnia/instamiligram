from .views import (
    HomeView,
    AboutView
)
from django.urls import path

app_name = "instagram"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about")
]
