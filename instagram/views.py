from typing import Any, Dict, List
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import CommentForm, CreatePostForm
from .models import Comment, Post, Like, Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator


class HomeView(LoginRequiredMixin, ListView):

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
                'post_type': 'following user posts'
            }
        )


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CreatePostForm()
        return render(
            request,
            'instagram/post_form.html',
            {
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST.get('tags')
            for tag_name in tags.split():
                if not Tag.objects.filter(name=tag_name).exists():
                    Tag.objects.create(name=tag_name)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'New Post!')
            return HttpResponseRedirect(
                reverse('instagram:post-detail', kwargs={"pk": post.pk})
            )
        return self.get(request)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        if post.author != request.user:
            return HttpResponseRedirect(reverse('instagram:home'))
        form = CreatePostForm(instance=post)
        return render(
            request,
            'instagram/post_form.html',
            {
                'form': form
            }
        )

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            tags = request.POST.get('tags')
            for tag_name in tags.split():
                if not Tag.objects.filter(name=tag_name).exists():
                    Tag.objects.create(name=tag_name)
            form.save()
            return HttpResponseRedirect(
                reverse('instagram:post-detail', kwargs={"pk": post.pk})
            )
        return self.get(request, pk)

    def test_func(self, pk):
        post = Post.objects.filter(id=pk).first()
        return self.request.user == post.author


class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        comments = post.comments.all()
        return render(
            request,
            "instagram/post_detail.html",
            context={
                'object': post,
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
        post_object_type = ContentType.objects.get_for_model(post)
        like_obj = Like.objects.filter(
            content_type=post_object_type, object_id=post.id, user=request.user
        )
        if like_obj.exists():
            liked = False
            like_obj.delete()
        else:
            liked = True
            like = Like.objects.create(
                content_type=post_object_type, object_id=post.id, user=request.user)
            like.save()

        result = post.total_likes
        post.save()

        return JsonResponse({'result': result, "liked": liked})


class LikeComment(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = int(request.POST.get('commentid'))
        comment = get_object_or_404(Comment, id=id)
        comment_object_type = ContentType.objects.get_for_model(comment)
        like_obj = Like.objects.filter(
            content_type=comment_object_type, object_id=comment.id, user=request.user
        )
        if like_obj.exists():
            liked = False
            like_obj.delete()
        else:
            liked = True
            like = Like.objects.create(
                content_type=comment_object_type, object_id=comment.id, user=request.user
            )
            like.save()
        result = comment.total_likes
        comment.save()
        return JsonResponse({'result': result, 'liked': liked})


class GlobalPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date_posted')
        return render(
            request,
            "instagram/home.html",
            context={
                'posts': posts,
            }
        )


class SavePost(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.profiles.filter(id=request.user.id).exists():
            post.profiles.remove(request.user.profile)
            saved = False
        else:
            post.profiles.add(request.user.profile)
            saved = True
        post.save()
        return JsonResponse({'saved': saved})


class SavedPostsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        p = Post.objects.all()
        posts = []
        for post in p:
            if post.profiles.filter(user=request.user).exists():
                posts.append(post)
        return render(
            request,
            "instagram/home.html",
            context={
                "posts": posts,
                'post_type': 'saved posts'
            }
        )


class SearchUser(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name').replace('@', '')
        users = User.objects.filter(username__contains=name).all()
        data = [user.username for user in users]
        return JsonResponse({'users': data})


class SearchTag(View):
    def post(self, request, *args, **kwargs):
        tag_name = request.POST.get('tag_name').replace('#', '')
        tags = Tag.objects.filter(name__startswith=tag_name).all()
        return JsonResponse({'tags': [tag.name for tag in tags]})


class UserLikedPostsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_object_type = ContentType.objects.get_for_model(Post)
        posts = []
        for post in Post.objects.all():
            if Like.objects.filter(content_type=post_object_type, object_id=post.id, user=request.user).exists():
                posts.append(post)
        return render(
            request,
            "instagram/home.html",
            {'posts': posts, 'post_type': 'liked posts'}
        )


class TagPostsView(LoginRequiredMixin, View):
    def get(self, request, tag):
        posts = Post.objects.filter(tags__contains=[tag])
        return render(
            request,
            "instagram/home.html",
            context={
                'posts': posts,
            }
        )
