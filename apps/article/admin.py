from django.contrib import admin
from article.models import Article, Label, Image


admin.site.register(Article)
admin.site.register(Label)
admin.site.register(Image)

