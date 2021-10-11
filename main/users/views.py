from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from django.views.generic import View

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
        messages.error(request,message="Check you info")
        return self.get(request=request)

class UserProfileView(View):
    
    def get(self,request,*args,**kwargs):
        return render(request,'users/profile.html')