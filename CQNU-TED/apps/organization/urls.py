# -*- coding: utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/18 15:40'
from django.urls import re_path, path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView


app_name = "organization"

urlpatterns = [

    # 课程机构列表url
    path('list/', OrgView.as_view(), name="org_list"),

    # 添加我要学习
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),

    # home页面,取纯数字
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),

    # 访问课程
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),

    # 访问机构描述
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),

    # 访问机构讲师
    re_path('org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),

    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),

    # 讲师列表
    re_path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),

    # 教师详情
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),


]
