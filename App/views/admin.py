from django.contrib import admin
from django.shortcuts import render, redirect
from App import models
from App.utils.encrypt import md5
from App.utils.form import AdminModelForm, AdminEditModelForm
from App.utils.page import PAGE


# Register your models here.
def admin_list(request):
    # 搜索功能
    search_dict = dict()
    value = request.GET.get("search", "")
    if value:
        search_dict["username__contains"] = value

    # 如果有搜索就会读取搜索之后的结果。所有的结果都会根据id排序
    admin_list = models.Admin.objects.filter(**search_dict).order_by("id")
    # 分页
    page_object = PAGE(request, admin_list, page_size=8)
    context = {
        "admin_list": page_object.page_queryset,  # 分完页的数据
        "search_data": value,  # 搜索之后的数据
        "page_string": page_object.create_html(),  # 生成的页码
        "search_page": page_object.search()  # 搜索功能
    }

    # 传送到前端
    return render(request, "admin_list.html", context)


def admin_add(request):
    # 如果没有信息POST过来，我们通过如下代码生成界面，等待POST
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "admin_add.html", {"form": form})
    form = AdminModelForm(data=request.POST)
    # 有数据POST过来之后
    # 如果数据通过了校验，保存数据
    if form.is_valid():
        form.save()
        return redirect("/chart/admin_list")
    # 如果数据没有通过校验，还是在添加界面，同时返回错误
    return render(request, "admin_add.html", {"title": "新建管理员", "form": form})


def admin_edit(request, nid):
    # 判断nid存不存在
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return render(request, 'error.html', {'msg': '数据不存在'})
    # 显示默认值
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_obj)
        return render(request, "admin_add.html", {"title": "编辑管理员", "form": form})
    form = AdminEditModelForm(instance=row_obj, data=request.POST)
    # 校验
    if form.is_valid():
        form.save()
        return redirect("/chart/admin_list")
    return render(request, "admin_add.html", {"title": "编辑管理员", "form": form})


def admin_del(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/chart/admin_list')


def admin_reset(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return render(request, 'error.html', {'msg': '数据不存在'})
    # 显示默认值
    row_obj.password = md5('123456')
    row_obj.save()
    return render(request, 'error.html', {'msg': '数据重置成功，{}现在的密码为默认密码123456'.format(row_obj.username)})
