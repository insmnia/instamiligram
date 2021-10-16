from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    CreateUserForm,
    UpdateProfileForm,
    UpdateUserForm
)
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
app_name = "user"


class CreateUserView(View):

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()

        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Successfully created")
            return redirect('login')
        messages.error(request, message="Check you info")
        return self.get(request=request)


class UserSettingsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            "user_form": UpdateUserForm(instance=request.user),
            "profile_form": UpdateProfileForm(instance=request.user)
        }
        return render(request, 'users/settings.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, message="Updated!")
            return redirect("user:settings")
        return self.get(request)


class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        return render(request, "users/profile.html", {"user": User.objects.filter(username=username).first()})


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_id = int(request.POST.get('id'))
        target_user = User.objects.filter(id=target_id).first()
        initiator_user = self.request.user
        # инициатор подписывается на таргет
        # пользователь уже подписан -> отписка
        flw = False
        if target_user.profile.followers.filter(id=initiator_user.id).exists():
            initiator_user.profile.following_count -= 1
            target_user.profile.followers_count -= 1
            target_user.profile.followers.remove(initiator_user)
            initiator_user.profile.following.remove(target_user)
            flw = False
        # подписка
        else:
            initiator_user.profile.following.add(target_user)
            target_user.profile.followers.add(initiator_user)
            initiator_user.profile.following_count += 1
            target_user.profile.followers_count += 1
            flw = True

        result = target_user.profile.followers_count
        initiator_user.profile.save()
        target_user.profile.save()
        return JsonResponse({"result": result, 'flw': flw})
