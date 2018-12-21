# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from apps.operation.models import UserFavorite,CourseComments,UserProfile
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
from .models import Course,CourseResource,Video
from apps.utils.mixin_utils import LoginRequiredMixin

from .models import Course, CourseResource
from apps.operation.models import UserFavorite, CourseComments, UserCourse
from apps.utils.mixin_utils import LoginRequiredMixin
from .models import Video
# Create your views here.
# 列表展示相关
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 2, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 是否收藏课程,在数据库中查找
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False

        # 必须是用户登录我们才能判断
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 课程标签
        # 通过当前标签，查找数据库中的课程
        tag = course.tag
        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:3]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 通过所有用户的id，找到所有用户学习的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses
        })


# 课程评论
class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all().order_by("-id")
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments

        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        # 使用request.user的形式进行确认登录状态
        if not request.user.is_authenticated:
            # 判断用户登录状态
            # 未登录返回json提示未登录，在Ajax中做登陆跳转
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id=int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')
# # 参考地址：http://www.cnblogs.com/sellsa/p/8641919.html

class VideoPlayView(LoginRequiredMixin, View):
    # 课程章节视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        # 通过外键找到章节再找到视频对应的课程
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否已经学习了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量前五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        # 资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request,'course-play.html',{
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,
        })
