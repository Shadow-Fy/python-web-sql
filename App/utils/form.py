from django import forms
from django.core.exceptions import ValidationError

from App import models
from App.utils.encrypt import md5


# 加入Bootstrap样式
class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class AdminModelForm(BootstrapModelForm):
    # 定义“确认密码”
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)  # 密码不一致之后，报错之后不置空
    )

    class Meta:
        model = models.Admin
        # confirm_password在输入密码时用于确认密码
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    # 确定是否存在此管理员
    def clean_username(self):
        text_admin = self.cleaned_data["username"]
        exists = models.Admin.objects.filter(username=text_admin).exists()
        if exists:
            raise ValidationError("管理员已存在")
        return text_admin

    # 加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 对比两次输入的密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        return confirm



class AdminEditModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)  # 密码不一致之后，报错之后不置空
    )
    username = forms.CharField(disabled=True, label="用户名")
    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 校验当前密码和新输入的密码是否一致
        # instance 就是传进来的对象，pk就是id
        exist = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exist:
            raise ValidationError('密码不能与之前的密码相同')
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        return confirm
