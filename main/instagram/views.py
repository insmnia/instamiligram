from typing import Any, Dict, List
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import CommentForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse


class HomeView(ListView):

    def get(self, request, *args, **kwargs):
        posts = []
        # список постов пользователей, НА которых подписан пользователь
        for u in request.user.profile.following.all():
            posts.extend(Post.objects.filter(author=u).all())
        return render(
            request,
            "instagram/home.html",
            context={
                'posts': posts,
                'form': CommentForm()
            }
        )

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.filter(id=id).first()
            comment.save()
            messages.success(request, message="Commented!")
        return self.get(request)


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


class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        comments = post.comments.all()
        return render(
            request,
            "instagram/post_detail.html",
            context={
                'post': post,
                'form': CommentForm(),
                'comments': comments,
            }
        )

    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.filter(id=pk).first()
            comment.save()
            messages.success(request, message="Commented!")
            return HttpResponseRedirect(reverse('instagram:post-detail', kwargs={"pk": pk}))


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
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        result = len(post.likes.all())
        post.save()

        return JsonResponse({'result': result, "liked": liked})


class GlobalPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "instagram/home.html",
            context={
                'posts': Post.objects.all(),
            }
        )


class SearchUser(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        users = User.objects.filter(username__contains=name).all()
        data = [user.username for user in users]
        return JsonResponse({'users': data})
