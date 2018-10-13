import time
import datetime

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.conf import settings
import json

from article.models import Article, Label, Image, Comment
from utils.mixin import LoginRequiredMixin


def time_ago(news):
    """
        处理时间
        显示为几年前，几天前，几个小时前。
    """
    # 得到整型系统时间戳
    sys_time = int(time.time())

    # 处理文章创建时间
    article_create_time = list()
    for new in news:
        create_time = new.create_time
        # 拿到格式为'2018-09-19 01:24:56'的部分。
        # 转换为time.struct_time()形式0
        ts = time.mktime(create_time.timetuple())
        # 得到创建时间的时间戳
        create_time = int((ts))
        diff_time = sys_time - create_time

        # 根据时间显示不同的规则
        year = int(diff_time / (3600*24*365))
        month = int(diff_time / (3600*24*30))
        day = int(diff_time / (3600*24))
        hour = int(diff_time / 3600)
        minute = int(diff_time / 60)

        if year >= 1:
            new.create_time = '%d年前' % year
        elif month >= 1:
            new.create_time = '%d月前' % month
        elif day >= 1:
            new.create_time = '%d天前' % day
        elif hour >= 1:
            new.create_time = '%d小时前' % hour
        elif minute >= 1:
            new.create_time = '%d分钟前' % minute
        else:
            new.create_time = '刚刚'

    return news


def article_index(request, label_id=None):
    """
        文章首页
        返回文章列表
        根据标签显示不同的列表
    """
    message = dict()
    label = Label.objects.all()
    message['labels'] = label
    if label_id is None:
        news = Article.objects.all().filter(statu=1).order_by('-create_time')
        news = time_ago(news)
        message['news'] = news
        message['active_new'] = 'active'
    else:
        news = Article.objects.all().filter(label_id=label_id, statu=1).order_by('-create_time')
        news = time_ago(news)
        message['news'] = news
        message['article_label'] = int(label_id)

    return render(request, 'index_bymyself.html', message)


def article_detail(request, article_id):
    """文章页面"""
    msg = dict()
    try:
        article = Article.objects.get(id=article_id)
        msg['article'] = article

        comment = Comment.objects.all().filter(article=article_id, status=0).order_by('-create_time')
        comment = time_ago(comment)  # 转换时间格式
        msg['comment'] = comment

        # 返回评论数量
        comment_num = len(comment)
        msg['comment_num'] = comment_num

        # 返回状态码
        if comment_num != 0:
            msg['status'] = 0  # 查询到了评论
        else:
            msg['status'] = 1  # 没有评论

    except Article.DoesNotExist:
        # 文章不存在
        # 这里可以制作一个404页面
        return redirect('article:index')

    return render(request, 'article.html', msg)


class ArticleComment(View, LoginRequiredMixin):
    """
        评论
    """
    def post(self, request, article_id):
        """
            提交评论
        """
        comment = request.POST.get('comment')
        article_id = article_id
        user = request.user

        msg = dict()
        try:
            comment = Comment.objects.create(article_id=article_id, user=user, comment=comment)
            comment.save()
            msg['status'] = 0
            return JsonResponse(msg)
        except Exception:
            msg['status'] = 1
            return JsonResponse(msg)


# 编辑器视图
class WangEditor(LoginRequiredMixin, View):
    """
        富文本编辑器
         wangEditor
    """
    def get(self, request):
        labels = Label.objects.all()
        # print(labels)
        return render(request, 'article_editor.html', {'labels': labels})

    def post(self, request):
        # 获取数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        label = request.POST.get('options')

        user = request.user  # 这里得到的是用户名

        # 验证数据的安全性
        # 验证数据是否为空
        if title == '':
            title = '无标题文章'

        # 检测数据库中是否存在'未分类'这个标签,如果没有就创建一个.
        try:
            label = Label.objects.get(label=label)
        except Label.DoesNotExist:
            try:
                label = Label.objects.get(label='未分类')
            except Label.DoesNotExist:
                label = Label.objects.create(label='未分类')
                label.save()

        # 存入数据库
        msg = dict()
        try:
            # 标签调整到个人主页操作.
            article = Article.objects.create(title=title, content=content, auther=user, label=label)
            article.save()
            msg['status'] = 'success'
            return JsonResponse(msg)
        except Exception:
            msg['status'] = 'fail'
            return JsonResponse(msg)


class EditView(View, LoginRequiredMixin):
    """
        对已经存在的文档进行修改
    """
    def get(self, request, article_id):
        # 查询文章对象返回
        article = Article.objects.get(id=article_id)
        # 查询所有标签返回
        labels = Label.objects.all()
        return render(request, 'article_editor_edit.html', {'article': article, 'labels': labels})

    def post(self, request, article_id):
        # 获取数据
        title = request.POST.get('title')
        label = request.POST.get('options')
        content = request.POST.get('content')
        # 验证数据的安全性
        # 验证数据是否为空
        if title == '':
            title = '无标题文章'

        msg = dict()

        # 检测数据库中是否存在'未分类'这个标签,如果没有就创建一个.
        try:
            label = Label.objects.get(label=label)
        except Label.DoesNotExist:
            try:
                label = Label.objects.get(label='未分类')
            except Label.DoesNotExist:
                label = Label.objects.create(label='未分类')
                label.save()

        # 存入数据库
        article = Article.objects.get(id=article_id)
        article.title = title
        article.label = label
        article.content = content
        article.save()
        msg['status'] = 'success'
        return JsonResponse(msg)


def delete(request, article_id):
    """删除文章"""
    # 验证用户和文章作者是否一致
    try:
        article = Article.objects.get(id=article_id)
        if request.user == article.auther:
            article.statu = 3
            article.save()
        return redirect('user:article')
    except:
        pass


class WangImg(LoginRequiredMixin, View):
    """编辑器图片上传"""
    def post(self, request):
        static_base = 'http://127.0.0.1:8000'
        static_url = static_base + settings.MEDIA_URL  # 上传文件展示路径前缀
        data = {
            "errno": 0,
            "data": [
                '',
            ],
        }  # 数据上传格式/json

        image_name = request.FILES.get('Image')
        if image_name:
            try:
                image = Image.objects.create(image=image_name)
                image.save()
                data['data'][0] = static_url + str(image.image)
                return HttpResponse(json.dumps(data))
            except Exception:
                data['errno'] = 1  # 错误类型1
                return HttpResponse(json.dumps(data))
        else:
            data['errno'] = 2  # 错误类型1
            return HttpResponse(json.dumps(data))


# @csrf_exempt
# def upload_image(request):
#     """
#         图片上传
#         tinymce
#     """
#     static_base = '//127.0.0.1:8000'
#     static_url = static_base + settings.MEDIA_URL  # 上传文件展示路径前缀
#     if request.method == 'POST':
#         # form = UploadImgForm(request.POST, request.FILES)
#         # print(form)
#         # if form.is_valid():
#         file = request.FILES['file']
#         print(file)
#         data = {'location': ''}
#         if file:
#             # 文件白名单
#
#             try:
#                 image = Image.objects.create(image=file)
#                 image.save()
#             except Exception:
#                 return HttpResponse(json.dumps(data))
#             location = static_url + str(image.image)
#             # data['data'].append(location)
#             data['location'] = location
#             return HttpResponse(json.dumps(data))
#         else:
#             return HttpResponse(json.dumps(data))


class UploadFile(View):
    """
        文件上传
    """
    def get(self, request):
        return render(request, 'test.html')

    def post(self, request):
        pass






