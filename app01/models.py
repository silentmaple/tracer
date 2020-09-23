from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.EmailField(verbose_name='邮箱地址', max_length=32)
    mobile = models.CharField(verbose_name='手机号', max_length=32)






