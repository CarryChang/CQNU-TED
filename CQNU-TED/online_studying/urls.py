"""online_studying path Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a path to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include,url
from django.views.generic import TemplateView  #导入view,表示处理的是静态文件
from apps.users.views import LogoutView, LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from django.views.generic import RedirectView
import xadmin
from apps.users.views import IndexView
from django.views.static import serve
from apps.organization.views import OrgView
from DjangoUeditor import urls as djud_urls
from online_studying.settings import MEDIA_ROOT
from apps.course.views import CourseDetailView


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    # 注册url
    path("register/", RegisterView.as_view(), name="register"),  # 通过类的as_view方法，调用这个view类
    path('', IndexView.as_view(), name="index"),
    # 退出功能url
    path('logout/', LogoutView.as_view(), name="logout"),
    # 验证码url
    path('captcha/', include('captcha.urls')),
    # 激活用户url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    # 忘记密码
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    # 重置密码url ：用来接收来自邮箱的重置链接
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),
    # 修改密码url; post提交的地方与get方式url中的地址不一样
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    # 课程机构app的url配置，讲师的也在里面
    path("org/", include('apps.organization.urls', namespace='org')),
    # 课程机构首页url
    # path('org_list/', OrgView.as_view(), name='org_list'),

    # 课程app的url配置
    path("course/", include('apps.course.urls', namespace="course")),
    # re_path('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$',  serve, {"document_root":STATIC_ROOT}),
    # user app的url配置
    path("users/", include('apps.users.urls', namespace="users")),
    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),
]
# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'






