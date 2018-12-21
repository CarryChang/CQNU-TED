# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.

# 城市信息和课程结构信息
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"学院名称")
    desc = UEditorField(verbose_name=u"学院描述",width=900, height=300, imagePath="org/ueditor/",
                                         filePath="org/ueditor/", default='')
    tag = models.CharField(default="全国知名", max_length=10, verbose_name=u"学院标签")
    category = models.CharField(default="pxjg", verbose_name=u"学院类别", max_length=20, choices=(("pxjg","大学"),("gr","个人"),("gx","研究生")))
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    # /media/org/2018/月份/图片名字
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"学院地址")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市",on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程学院"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        # 获取学院的教师数
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


# 讲师
class Teacher(models.Model):
    # 一个学院会有很多老师，所以我们在讲师表添加外键并把课程学院名称保存下来
    # 可以使我们通过讲师找到对应的学院
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属学院",on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职学校")
    work_position = models.CharField(max_length=50, verbose_name=u"教师级别")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    age = models.IntegerField(default=25, verbose_name=u"年龄")
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name=u"头像", max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师: {1}".format(self.org, self.name)

    def get_course_nums(self):
        return self.course_set.all().count()


