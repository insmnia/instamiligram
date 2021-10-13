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


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            "user_form": UpdateUserForm(instance=request.user),
            "profile_form": UpdateProfileForm(instance=request.user)
        }
        return render(request, 'users/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, message="Updated!")
            return redirect("user:profile")
        return self.get(request)
