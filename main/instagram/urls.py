from .views import (
    AboutView,
    PostCreateView,
    PostListView,
    PostDetailView,
    UserPostListView,
    PostUpdateView,
    PostDeleteView
)
from django.urls import path

app_name = "instagram"

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("post/new/",PostCreateView.as_view(),name="post-create"),
    path("post/<int:pk>/",PostDetailView.as_view(),name="post-detail"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
]
