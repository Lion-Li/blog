import re

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from user.models import  UserProfile
from utils.mixin import LoginRequiredMixin
from article.models import Article, Label
from article.views import time_ago


def test(request):
    """测试页面"""
    return render(request, 'test.html')


class LoginView(View):
    """
        登录
        get显示登录页面
        post校验用户
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)

        # 校验用户名和密码是否为空
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '请输入用户名和密码'})

        # 校验失败,返回None.
        user = authenticate(username=username, password=password)
        if user is not None:
            # 如果账户已激活
            if user.is_active == 1:
                # 使用django内置login函数将用户登录信息记录在session中
                login(request, user)
                return redirect('article:index')
            else:
                return render(request, 'login.html', {'errmsg': '请联系管理员激活用户'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class LogoutView(View):
    """注销"""
    def get(self, request):
        logout(request)
        return redirect('user:login')


class RegisterView(View):
    """
        注册
        get显示注册页面
    """
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        email = request.POST.get('email')
        # yzm = request.POST.get('yzm')
        # verifycode = request.session['verifycode']
        # allow = request.POST.get('allow')

        # 验证数据
        # 数据的校验应该在表单就应该校验完成,格式不正确不予提交,减少服务器的工作量.
        # 目前存在格式不正确,但是能够提交表单,从而引发错误的问题,待修正.

        if not all([username, password, password_again, email]):
            return render(request, 'register.html', {'errmsg': '请填写完所有信息'})

        if password != password_again:
            return render(request, 'register.html', {'errmsg': '两次密码输入不一致,请重输!'})

        if not re.match(r'^[a-zA-Z0-9][\w._-]*@[a-zA-Z0-9_-]+(.[a-zA-Z0-9]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 提交前,检查用户名是否存在.
        same_username = UserProfile.objects.all().filter(username=username)
        if same_username:
            return render(request, 'register.html', {'errmsg': '用户名已存在!'})

        usr = UserProfile.objects.create_user(username, email, password)
        usr.is_active = 1
        usr.save()
        return redirect('user:login')
        # if allow != 'on':
        #     return render(request, 'register.html', {'errmsg': '不同意协议无法为您服务'})

        # 校验验证码
        # if yzm.upper() != verifycode:
        #     return render(request, 'register.html', {'errmsg': '验证码错误'})
        # else:
        #     # 验证码通过后再将用户信息保存到数据库
        #     usr = User.objects.create_user(username, email, password)
        #     usr.is_active = 0
        #     usr.save()
        #     # 发送激活链接
        #     info = {'confirm': usr.id}
        #     verify_email = Verify()
        #     token = verify_email.encypt_info(info)
        #     # 发送邮件
        #     send_register_email.delay(email, username, token)


# class UserCenter(View, LoginRequiredMixin):
#     """个人中心"""
    # def get(self, request):
    #     user = request.user
    #     articles = Article.objects.all().filter(auther=user).order_by('-create_time')
    #     return render(request, 'user_article.html', {'articles': articles})

def user_article(request, auther_id=None):
    """用户的主页"""
    message = dict()
    # 查询所有标签对象返回
    label = Label.objects.all()
    message['labels'] = label
    if auther_id is None:
        # 查询用户对象返回
        user = request.user
        message['auther'] = user.username

        articles = Article.objects.all().filter(auther=user, statu=1).order_by('-create_time')
        articles = time_ago(articles)
        message['articles'] = articles
    else:
        # 查询用户对象返回
        auther = UserProfile.objects.get(id=auther_id)
        message['auther'] = auther

        articles = Article.objects.all().filter(auther=auther_id, statu=1).order_by('-create_time')
        articles = time_ago(articles)
        message['articles'] = articles
    # 激活最新标签
    message['active'] = 'active'

    return render(request, 'user_article.html', message)


# def user_article_label(request, auther_id=None, label_id=None):
#     message = dict()
#     label = Label.objects.all()
#     message['labels'] = label
#     if auther_id is not None:
#         if label_id is None:
#             articles = Article.objects.all().filter(auther_id=auther_id).order_by('-create_time')
#             message['articles'] = articles
#             message['active_new'] = 'active'
#         else:
#             articles = Article.objects.all().filter(auther_id=auther_id, label_id=label_id).order_by('-create_time')
#             message['articles'] = articles
#             message['article_label'] = int(label_id)
#     else:
#         user = request.user
#         if label_id is None:
#             articles = Article.objects.all().filter(auther=user).order_by('-create_time')
#             message['articles'] = articles
#             message['active_new'] = 'active'
#         else:
#             articles = Article.objects.all().filter(auther=user, label_id=label_id).order_by('-create_time')
#             message['articles'] = articles
#             message['article_label'] = int(label_id)
#
#     return render(request, 'user_article.html', message)
#

