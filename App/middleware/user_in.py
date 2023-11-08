# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class UserInMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 获取当前用户请求的url，如果访问的是login直接放行，不然会死递归
        if request.path_info == '/login':
            return
        # 读取当前用户的session信息
        info_dict = request.session.get('info')
        # 证明用户已经登录了
        if info_dict:
            return
        # 证明用户没登录
        return redirect('/login')
