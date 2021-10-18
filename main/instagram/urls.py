from .views import (
    AboutView,
    LikeComment,
    PostCreateView,
    HomeView,
    PostDetailView,
    SavePost,
    SavedPostsView,
    UserLikedPostsView,
    UserPostListView,
    PostUpdateView,
    PostDeleteView,
    LikeView,
    GlobalPostView,
    SearchUser,
    TagPostsView
)
from django.urls import path
app_name = "instagram"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path("like/", LikeView.as_view(), name="like"),
    path('explore', GlobalPostView.as_view(), name="explore"),
    path('search', SearchUser.as_view(), name='search'),
    path('save',SavePost.as_view(),name="save"),
    path('post/saved',SavedPostsView.as_view(),name="post-saved"),
    path('likecom/',LikeComment.as_view(),name='like-com'),
    path('liked/',UserLikedPostsView.as_view(),name='post-liked'),
    path('post/tag/<str:tag>',TagPostsView.as_view(),name='post-tag'),
]
