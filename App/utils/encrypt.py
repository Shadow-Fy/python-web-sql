# -*- coding:utf-8 -*-
from django.conf import settings
import hashlib

# 加密
def md5(data):
    # SECRET_KEY是Django自带的
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data.encode("utf-8"))
    return obj.hexdigest()
