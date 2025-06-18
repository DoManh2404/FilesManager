import os.path
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from myapp import forms


def index(request):
    try:
        return HttpResponse("haha")
    except Http404:
        return HttpResponse('404')


def data_reg(request):
    return None


def data_int(request):
    return None