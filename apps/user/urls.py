from django.urls import path, re_path

from user.views import LoginView, RegisterView, LogoutView, user_article

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # re_path(r'article/(?P<label_id>\d+)$', user_article, name='form_my_index'),

    # 返回用户的主页
    re_path(r'^article/(?P<auther_id>\d+)$', user_article, name='article_auther'),
    path('article/', user_article, name='article'),

    # path('', test, name='test'),
    # path('login/', views.login, name='login'),
]
