# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from apps.course.models import Course
from apps.users.models import UserProfile

# Create your models here.
# 用户咨询
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(models.Model):
    #  课程评论  设计两个外键：1.用户 2.课程
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u"课程",on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程评论"
        verbose_name_plural = verbose_name


# 用户对于课程，学院，讲师的收藏
class UserFavorite(models.Model):
    # 涉及四个外键。用户，课程，学院，讲师
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id") # 直接保存用户id
    fav_type = models.IntegerField(choices=((1,"课程"), (2,"课程学院"),(3,"讲师")), default=1, verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # 因为我们的消息有两种:发给全员和发给某一个用户。
    # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。

    # 机智版 为0发给所有用户，不为0就是发给用户的id
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    # 两个外键：1.用户，2.课程.
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u"课程",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name