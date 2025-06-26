# middleware_sample/middlewares.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import re

url_list = [
    '/admin/',
    '/login/',
    '/test/',
    '/api/',
    '/signup/'
]


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        v_path = request.path
        is_authenticated = request.user.is_authenticated
        
        start_with_url = any(v_path.startswith(url) for url in url_list)
        if not start_with_url and not is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return self.get_response(request)
        
