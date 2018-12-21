# _*_ encoding:utf-8 _*_
# 第一个区域，放python自带的包
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models
# from django.contrib.auth.models import AbstractUser

# 继承Django自身的AbstractUser,沿用默认字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male",u"男"),("female","女")), default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True,verbose_name='手机号')
    # 增加用户头像字段，img/%Y/%m代表上传时按年月文件夹进行，default设置的是默认头像路径
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png", max_length=100, verbose_name='头像')
    class Meta:
        verbose_name = "用户信息"  # 设置UserProfile这个类的别名
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username  # 当使用print打印时，把继承的username字段打印出来

# 邮箱验证码
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email",u"修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)
    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    # 默认index很大靠后。想要靠前修改index值
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

