from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """用户模型类"""

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
