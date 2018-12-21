# _*_ encoding:utf-8 _*_
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # Q可以帮助实现并集
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm
from apps.utils.email_send import send_register_email  # import 发邮件函数
from apps.utils.mixin_utils import LoginRequiredMixin
from apps.operation.models import UserCourse, UserFavorite, UserMessage
from apps.organization.models import CourseOrg, Teacher
from apps.course.models import Course
from .models import Banner


# 实现用户名、邮箱均可登录
# 继承ModelBackend类。因为他有方法authenticate，可点进源码查看
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 通过username或Email查询用户 ,用username或者Email对传入的username进行匹配
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 判断密码是否一致
            # django的后台中密码加密：所以不能 password==password
            # UserProfile继承的AbstractUser中 def check_password(self,raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        # active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_records:
            for record in all_records:
                # 获取对应的邮箱
                email = record.email
                # 获取邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功页面，跳转到登录页面
                return render(request, "login.html")
        # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request, "active_fail.html")


# 创建一个注册的类
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()  # 实例化RegisterForm
        return render(request, "register.html", {'register_form': register_form})   # 将register_form传入register.html

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():

            user_name = request.POST.get("email", "")
            # 如果用户已经存在 提出错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")  # 取出POST中的password
            user_profile = UserProfile()  # 实例化UserProfile对象
            user_profile.username = user_name  # 将POST中取出的username传给UserProfile实例中的username
            user_profile.email = user_name  # 将POST中取出的username传给UserProfile实例中的emil
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)  # 对保存到数据库的密码加密
            user_profile.save()  # 保存到数据表

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册重师网络教学平台"
            user_message.save()

            send_register_email(user_name, "register")  # 发送邮件
            return render(request, "login.html")  # 如果验证成功，则跳转到登录页面
        else:
            return render(request, "register.html", {"register_form": register_form})  # 若验证失败返回注册页面返回register_form错误信息


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


# 用户登录
class LoginView(View):
    def get(self, request):  # 重写View的GET方法
        return render(request, "login.html", {})  # 将user_login函数的GET判断分支的代码拉过来

    def post(self, request):
        login_form = LoginForm(request.POST)  # 实例化LoginForm类的对象，需传入request.POST参数
        if login_form.is_valid():  # 检查login_form是否出错，没出错的才验证用户名和密码
            # 获取用户提交的用户名和密码
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 成功返回user对象，
            user = authenticate(username=user_name, password=pass_word)  # 利用django自带的authenticate方法来确认这个用户是否合法，
            if user is not None:    # 如果该用户合法，则user非空
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
            # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"}, {"login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})  # 如果login_form出错,则返回login_form对象，在前端做进一步处理


# 用户忘记密码 找回密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    # post方法实现
    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        # form验证合法情况下取出Email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                # 获取对应的邮箱
                email = record.email
                # 将Email传回来
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 修改密码
class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})

class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        # 上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses":user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            teacher = Course.objects.get(id=course_id)
            course_list.append(teacher)
        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list
        })


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages":messages
        })


class IndexView(View):
    # 重师网络教学平台 首页
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response