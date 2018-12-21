# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField
from apps.organization.models import CourseOrg, Teacher

# 课程信息表
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = UEditorField(verbose_name=u"课程详情",width=600, height=300, imagePath="courses/ueditor/",filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    degree = models.CharField(verbose_name=u"难度", choices=(("cj","初级"), ("zj","中级"), ("gj","高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属学院", null=True, blank=True)
    category = models.CharField('课程类别', max_length=20, default='')
    tag = models.CharField('课程标签', default='', max_length=10)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, on_delete=models.CASCADE, blank=True)
    youneed_know = models.CharField("上课须知", max_length=300, default='')
    teacher_tell = models.CharField('悄悄告诉你', max_length=300, default='')
    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
    def get_zj_nums(self):
        # 获取课程的章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'  # 在后台显示的名称
    def go_to(self):
        from django.utils.safestring import mark_safe
        # mark_safe后就不会转义
        return mark_safe("<a href='https://home.cnblogs.com/u/derek1184405959/'>跳转</a>")
    go_to.short_description = "跳转"

    def get_course_lesson(self):
        # 获取课程的章节
        return self.lesson_set.all()
    def get_learn_users(self):
        # 获取这门课程的学习用户
        return self.usercourse_set.all()[:5]

    def __str__(self):
        return self.name


class BannerCourse(Course):
    # 显示轮播课程
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会在生成一张表，而且具有Model的功能
        proxy = True

# lesson章节
class Lesson(models.Model):
    # 因为一个课程对应很多章节。所以在章节中将课程设置为外键
    # 作为一个字段来让我们可以知道这个章节对应哪个课程
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name
    def get_lesson_video(self):
        # 获取章节所有视频
        return self.video_set.all()

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


# video
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
# CourseResource 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
# Videoup 上传视频,写完之后记得对数据库进行更新（先makemigrations,再migrate）
class Videoup(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    upload = models.FileField(upload_to='video/', verbose_name=u"视频文件", max_length=100)
    class Meta:
        verbose_name = u"上传视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name