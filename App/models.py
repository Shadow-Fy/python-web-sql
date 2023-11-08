from django.db import models


# Create your models here.
class MoviesInfo(models.Model):
    title = models.CharField(max_length=32)
    director = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    rating = models.FloatField()
    judge = models.FloatField()
    inq = models.CharField(max_length=64)

class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)