from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **fields):
        if not email:
            raise ValueError("이메일 주소 필수")
        user = self.model(email=self.normalize_email(email), name=name, **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, blank=False)
    name = models.CharField(max_length=16, unique=True, blank=False)
    sex = models.CharField(max_length=1, null=True)
    age = models.IntegerField(null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    objects = CustomUserManager()  # 사용자 정의 매니저 정의,

    @property
    def is_staff(self):
        return self.is_admin

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]