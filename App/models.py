from django.db import models


# Create your models here.
class MoviesInfo(models.Model):
    zh_name = models.CharField(max_length=15)  # 中文名
    en_name = models.CharField(max_length=70)  # 英文名
    director = models.CharField(max_length=70)  # 导演
    actor = models.CharField(max_length=50)  # 演员
    release_year = models.IntegerField()  # 上映年份
    release_country = models.CharField(max_length=30)  # 上映国家
    type = models.CharField(max_length=30)  # 类型
    score = models.CharField(max_length=3)  # 评分
    eval_number = models.CharField(max_length=10)  # 评价人数
    quotation = models.CharField(max_length=50)  # 语录


class CountryCount(models.Model):
    release_country = models.CharField(max_length=30)
    country_count = models.IntegerField()


class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
