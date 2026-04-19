
from django.shortcuts import render, redirect
from django.views import View
from users.forms import RegisterForm, RegisterModelForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


class RegisterView(View):
    template_name = 'users/register.html'
    def get(self, request):
        return render(request, self.template_name, context={'form': RegisterForm()})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request, self.template_name, context={'form': form})
class LoginView(View):
    template_name = 'users/login.html'
    def get(self, request):
        return render(request, self.template_name, context={'form': LoginForm()})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:index')
        return render(request, self.template_name, context={'form': form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main:index')