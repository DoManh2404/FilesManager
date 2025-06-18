from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import MyUser
from django.contrib.auth import get_user_model

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
            return HttpResponseBadRequest("Bad Request Message")


User = get_user_model()

class SignUpView(View):
    def post(self, request, *args, **kwargs):
        try:
            uName = request.POST.get('userID')
            uPasswork = request.POST.get('userPW')
            uEmail = request.POST.get('userEmail')

            if not uName or not uPasswork or not uEmail:
                return HttpResponse("Data input null")

            if User.objects.filter(username=uName).exists():
                return HttpResponse("Username already exists")
            if User.objects.filter(email=uEmail).exists():
                return HttpResponse("Email already exists")

            user = User.objects.create_user(username=uName, password=uPasswork, email=uEmail)
            user.save()
            return redirect('home')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Bad Request Message")

    def get(self, request, *args, **kwargs):
        return render(request, 'myapp/login.html')


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

