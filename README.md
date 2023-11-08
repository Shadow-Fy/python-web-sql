# python+SQL+Django+Web大作业

### 项目简介：

使用 Python 进行爬虫爬取一些数据，然后利用百度开源的纯 Javascript 图表库 ECharts 对数据进行可视化，利用 Django 将数据展示在Web中。



### 数据库操作：

 在终端启动MySQL：

```shell
net start mysql
```

 登录MySQL，并输入密码：

```shell
mysql -u root -p
```

创建名为test的数据库：

```sql
 create database test DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

 查看是否创建：

```sql
show databases;
```

##### 增

 在setting.py中 进行配置和修改。我们不用Django默认的数据库（sqlite3），我们用自己的。记得改数据库的名字、用户和密码。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '******',#密码就不展示了
        'HOSR': '127.0.0.1',
        'POST': '3306',
    }
}
```

我们先在model.py中加入如下代码，Django会将这个类中的指令转化为SQL语句

```python
from django.db import models

# Create your models here.
# 写一个继承models.Model的类
class Movies(models.Model):
    title = models.CharField(max_length=32)
    director = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    rating = models.FloatField()
    judge = models.FloatField()
    inq = models.CharField(max_length=64)

```

写完配置在终端中输入命令执行的。

```python
python manage.py makemigrations
python manage.py migrate
```

使用目标表：

```powershell
use test;
```

查看表内容：

```c#
show tables;
```



##### 删

直接把对应的类注释掉，然后再执行一下`makemigrations`和` migrate`语句，那个表就没了。



##### 改

直接在class里面修改，最后再执行一下`makemigrations`和` migrate`语句。

 注意：安全起见，Django在增加列的时候会设置选项，第一个选项为新列赋初值，第二个选项是取消增加列。



#### 加入数据

在views.py中建立页面：

```python
def orm(request):
    from blog.models import StudentInfo
    StudentInfo.objects.create(name="Clark", height=182, weight=68, age=20)
    StudentInfo.objects.create(name="Olsen", height=168, weight=50, age=33)
    return HttpResponse("success!!")

```













### 遇到的问题总结：

#### Django 无法显示 css 样式

在测试 Django 时，浏览器打开的html页面发现没有css样式（css无法渲染html网页），但是直接打开 html 文件时是可以正常打开的，查找了各种方法后最终得以解决：

首先可以尝试更改文件目录，如图所示，CSS类型的文件由 CSS 文件管理，然后放在 static 文件内，注意 static 文件的目录位置，放错了可能就导致出现问题，尝试过放在其他位置无法显示 css 样式（和 templates 在同一目录下）

![image-20231025213500373](https://img2023.cnblogs.com/blog/2821249/202310/2821249-20231025214226415-367381709.png)

然后更改创建 Django 项目时自带的 setting.py 文件，翻到最下面修改，具体如下：

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ] # 多了这一行
```



如果经过上述操作仍然无效，请删除 html 文件中的 `<!DOCTYPE html>` ，最后是到这里就成功了