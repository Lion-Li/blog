"""WeBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from article import views
from article.views import WangEditor, WangImg


urlpatterns = [
    path('admin/', admin.site.urls),

    # 测试WangEditor
    path('img', WangImg.as_view(), name='Img'),
    path('test/', WangEditor.as_view()),

    path('user/', include('user.urls')),
    path('article/', include('article.urls')),
    path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    path('', views.article_index),  # 显示首页
]

# mdeditor配置
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
