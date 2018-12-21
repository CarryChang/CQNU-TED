# -*- coding: utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/17 17:11'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


# 检验从前台传来的表单是否合法,并提醒用户正确输入
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 将username设为必填字段
    password = forms.CharField(required=True, min_length=5)  # 将password设置为必填字段，且最短长度是5


# 注册验证表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})  # 增加error_message中的invalid的中文写法


# 忘记密码
class ForgetPwdForm(forms.Form):
    # 此处Email与前端name需保持一致
    email = forms.EmailField(required=True)
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


# 修改密码的form表单
class ModifyPwdForm(forms.Form):
    """重置密码"""
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']

