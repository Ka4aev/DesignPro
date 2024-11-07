from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=254, verbose_name="Имя")
    patronymic = models.CharField(max_length=254,blank=True, verbose_name="Отчество")
    last_name = models.CharField(max_length=254, verbose_name="Фамилия")
    username = models.CharField(max_length=254, verbose_name="Логин", unique=True)
    email = models.EmailField(max_length=254, verbose_name="Почта", unique=True)
    password = models.CharField(max_length=254, verbose_name="Пароль")

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.fio