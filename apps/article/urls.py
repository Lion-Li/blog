from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from article import views
from article.views import WangEditor, WangImg, EditView, UploadFile, ArticleComment

app_name = 'article'
urlpatterns = [
    # 请求文章内容+评论
    re_path(r'^details/(?P<article_id>\d+)/$', views.article_detail, name='details'),

    # 提交评论
    # path('details/<article_id>/comment)', ArticleComment, name='comment_submit'),
    re_path(r'^comment/submit/(?P<article_id>\d+)/$', ArticleComment.as_view(), name='comment_submit'),

    # re_path(r'^details/(?P<article_id>\d+)/$', include([
    #     path('comment/', ArticleComment, name='comment'),
    #     path('', views.article_detail, name='details'),
    # ])),
    # 删除评论
    # re_path(r'^comment/delete/(?P<article_id>\d+)$', views.article_detail, name='details'),


    # 编辑器
    # 图片上传
    path('editor/image', WangImg.as_view(), name='image'),
    path('editor/', WangEditor.as_view(), name='editor'),

    # 文件上传
    path('editor/file', UploadFile.as_view(), name='file'),

    # 编辑文章
    re_path(r'^edit/(?P<article_id>\d+)$', EditView.as_view(), name='edit'),
    path('editor/edit/image', WangImg.as_view(), name='image'),

    # 删除文章
    re_path(r'^delete/(?P<article_id>\d+)$', views.delete, name='delete'),


    re_path(r'^index/(?P<label_id>\d+$)', views.article_index, name='index_label'),
    path('', views.article_index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
