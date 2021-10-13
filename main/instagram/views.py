from typing import List
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "instagram/home.html"
    ordering = ['-date_posted']


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = "instagram/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", 'content', 'image']

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDetailView(DetailView):
    model = Post


class AboutView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "instagram/about.html")


class UserPostListView(ListView):
    model = Post
    template_name = "instagram/user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.likes_count -= 1
        else:
            post.likes.add(request.user)
            post.likes_count += 1

        result = post.likes_count
        post.save()

        return JsonResponse({'result': result, })
