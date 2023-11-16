from multiprocessing import connection

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from App import models
from App.models import MoviesInfo, CountryCount
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


def get_movie_data(request):
    movie_data = MoviesInfo.objects.all()

    data = []

    for entry in movie_data:
        data.append({
            'zh_name': entry.zh_name,
            'en_name': entry.en_name,
            'director': entry.director,
            'actor': entry.actor,
            'release_year': entry.release_year,
            'release_country': entry.release_country,
            'type': entry.type,
            'score': entry.score,
            'eval_number': entry.eval_number,
            'quotation': entry.quotation,
        })
    return JsonResponse(data, safe=False)


def get_country_count(request):
    country_count_data = CountryCount.objects.values('release_country', 'country_count')
    country_count_list = list(country_count_data)
    return JsonResponse(country_count_list, safe=False)
