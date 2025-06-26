from django.views import View
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import MyUser


class LoginView(View):
    def get(self, request):
        return render(request, 'myapp/login.html')

    def post(self, request):
        try:
            username = request.POST.get('userID')
            password = request.POST.get('userPW')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'myapp/login.html')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(str(e))


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myapp/login.html')

    def post(self, request, *args, **kwargs):
        try:
            u_name = request.POST.get('userID')
            u_passwork = request.POST.get('userPW')
            u_email = request.POST.get('userEmail')

            if not u_name or not u_passwork or not u_email:
                messages.error(request, 'Data input null')
                return render(request, 'myapp/login.html', {'show_signup': True})
            if MyUser.objects.filter(username=u_name).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'myapp/login.html', {'show_signup': True})
            if MyUser.objects.filter(email=u_email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'myapp/login.html', {'show_signup': True})

            user = MyUser.objects.create_user(username=u_name, password=u_passwork, email=u_email)
            user.save()
            messages.success(request, 'Created user successfully')
            return render(request, 'myapp/login.html')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(str(e))


class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            return redirect('login')
        except Http404:
            return HttpResponseBadRequest()


class HomeView(View):
    def get(self, request):
        try:
            return render(request, 'myapp/home.html')
        except Http404:
            return HttpResponseBadRequest()
