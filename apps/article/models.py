from datetime import datetime

from django.db import models
from tinymce.models import HTMLField

from user.models import UserProfile


class Article(models.Model):
    """文章模型类"""
    choices = (
        (0, '未发布'),
        (1, '已发布'),
        (2, '撤销'),
        (3, '删除'),
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    content = HTMLField(default='', verbose_name='内容')
    image = models.ImageField(upload_to='article/%Y/%m/',default='', blank=True, verbose_name='图片')
    auther = models.ForeignKey(UserProfile, verbose_name='作者', on_delete=models.CASCADE)
    label = models.ForeignKey('Label', verbose_name='栏目', on_delete=models.CASCADE)
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    statu = models.IntegerField(choices=choices, default=1, verbose_name='状态')

    class Meta:
        db_table = 'article'
        verbose_name = '文章信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Label(models.Model):
    """分类"""
    label = models.CharField(max_length=100, verbose_name='分类')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.label


class Image(models.Model):
    """图片"""
    image = models.ImageField(upload_to='article/%Y/%m', verbose_name='图片')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """评论Model"""
    choices = (
        (0, '已发布'),
        (1, '已删除'),
    )
    article = models.ForeignKey(Article, verbose_name='所属文章', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='所属用户', on_delete=models.CASCADE)
    comment = models.TextField(default='无内容', verbose_name='评论')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.IntegerField(choices=choices, default=0, verbose_name='状态')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

