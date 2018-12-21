# -*- coding: utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/18 15:40'
from django.conf.urls import url, include
from django.urls import re_path,path
from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, ResetView
from .views import UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MymessageView,ActiveUserView


app_name = 'users'
urlpatterns = [

    # 激活用户url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name= "user_active"),

    # 重置密码urlc ：用来接收来自邮箱的重置链接
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),

    # 用户信息
    path('info/', UserinfoView.as_view(), name="user_info"),

    # 用户头像上传
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),

    # 用户个人中心修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),

    # 发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),

    # 修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),

    # 用户中心我的课程
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),

    # 我收藏的课程机构
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),

    # 我收藏的授课讲师
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我收藏的课程
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息
    path('my_message/', MymessageView.as_view(), name="my_message"),
]


