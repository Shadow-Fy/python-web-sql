from django.shortcuts import render, HttpResponse, redirect
from django import forms
from App.utils.encrypt import md5
from App import models
from io import BytesIO
from App.utils.create_image import get_image


class LoginForm(forms.Form):
    username = forms.CharField(label='USERNAME',
                               widget=forms.TextInput(attrs={
                                   'name': "username",
                                   'class': "border-item",
                                   'autocomplete': "off"}),
                               required=True  # 这是默认的，代表必填
                               )
    password = forms.CharField(label='PASSWORD',
                               widget=forms.PasswordInput(  # 用我们白嫖过来的样式
                                   {'name': "password",
                                    'class': "border-item",
                                    'autocomplete': "off"},
                                   render_value=True  # 保留密码
                               ),
                               required=True  # 这是默认的，代表必填
                               )

    # 返回密文
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    # 这部分纯粹就是尝试这个用法，在这个小问题上没有特别大的实际作用
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["placeholder"] = field.label


# 登录界面
# 登录界面
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 这里是没有models.save的，但是form.cleaned_data
        # 直接用字典形式，不用一个一个写
        admin_exist = models.Admin.objects.filter(**form.cleaned_data).first()
        # 密码错误
        if not admin_exist:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        # 生成随机cookie原来还是比较麻烦的事情，但是Django帮我们简化了
        # 这一行代码直接完成了cookie的随机字符串的生成，将随机字符串保存到session中并附上响应的值
        request.session['info'] = {'id': admin_exist.id, 'username': admin_exist.username}
        return redirect("/chart/")
    return render(request, 'login.html', {"form": form})


def image_code(request):
    img, code = get_image()
    # 考虑到多用户访问
    request.session['image_code'] = code
    # 设置60秒后超时
    request.session.set_expiry(60)
    # 直接存内存里
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
