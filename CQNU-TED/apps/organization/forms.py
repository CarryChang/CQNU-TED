# -*- coding: utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/18 15:03'

import re
from django import forms

from apps.operation.models import UserAsk


# 用ModelForm来实现，提交我要学习咨询
class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 手机号验证的正则表达式验证
    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
