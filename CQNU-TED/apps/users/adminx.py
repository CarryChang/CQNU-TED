# -*- coding: utf-8 -*-

import xadmin
from .models import UserProfile, EmailVerifyRecord, Banner
from xadmin import views

class UserProfileAdmin:
    pass


# 邮箱验证码中增加列表项 ,创建管理类，继承object
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 基本的修改
class BaseSetting(object):
    enable_themes = True   # 打开主题功能
    use_bootswatch = True  # 设置后才有很多主题可用

# 针对全局的 头和页脚
class GlobalSettings(object):
    site_title = "在线学习后台管理系统"  # 系统名称
    site_footer = "CQNU-TED"  # 底部版权栏
    menu_style = "accordion"     # 将菜单栏收起来

# 将model与admin管理器进行关联注册
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 注册，注意一个是BaseAdminView，一个是CommAdminView
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)



