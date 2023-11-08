from django.http import HttpResponse
from django.shortcuts import render, redirect

from App import models
from App.utils.form import AdminModelForm
from App.utils.page import PAGE


# Create your views here.
def empty(request):
    return render(request, 'empty.html')


def Login(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    if username == "root" and password == "root":
        return redirect("/chart")
    return render(request, "login.html", {"error_msg": "用户名或密码错误"})


# -*- coding:utf-8 -*-
def chart_list(request):
    return render(request, 'chart_list.html')


def home(request):
    return render(request, 'home.html')

