# Generated by Django 2.1.1 on 2018-09-30 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20180929_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='show',
            new_name='statu',
        ),
        migrations.AlterField(
            model_name='label',
            name='label',
            field=models.CharField(default='未分类', max_length=100, verbose_name='分类'),
        ),
    ]