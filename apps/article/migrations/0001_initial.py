# Generated by Django 2.1.1 on 2018-09-26 16:05

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('content', tinymce.models.HTMLField(default='', verbose_name='内容')),
                ('image', models.ImageField(upload_to='article/%Y/%m/', verbose_name='')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击量')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '文章信息',
                'db_table': 'article',
                'verbose_name': '文章信息',
            },
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='article/%Y/%m', verbose_name='图片')),
            ],
            options={
                'verbose_name_plural': '图片',
                'verbose_name': '图片',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='分类')),
            ],
            options={
                'verbose_name_plural': '分类',
                'verbose_name': '分类',
            },
        ),
    ]