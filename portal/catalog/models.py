from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    fio = models.CharField(max_length=254, verbose_name="ФИО")
    username = models.CharField(max_length=254, verbose_name="Логин", unique=True)
    email = models.EmailField(max_length=254, verbose_name="Почта", unique=True)
    password = models.CharField(max_length=254, verbose_name="Пароль")

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.fio