from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User


class RegisterView(View):
    template_name = 'users/register.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(raw_password=password)
        user.save()
        return redirect('users:login')

class LoginView(View):
    template_name = 'users/login.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass