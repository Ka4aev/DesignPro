from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
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
        return f"{self.last_name} {self.first_name} {self.patronymic}"


def validate_image(image):
    # Проверка MIME типа файла
    valid_mime_types = ['image/jpeg', 'image/png', 'image/bmp']
    mime_type = getattr(image.file, 'content_type', None)
    if mime_type:
        if mime_type not in valid_mime_types:
            raise ValidationError("Формат файла должен быть: jpg, jpeg, png, bmp.", code='invalid_mime_type')
    else:
        raise ValidationError("Не удалось определить формат файла.", code='unknown_mime_type')

    # Проверка размера файла
    file_size = image.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2 МБ.", code='file_too_large')

    # Проверка разрешения изображения
    try:
        img = Image.open(image)
        img.verify()  # Проверка целостности изображения

        width, height = img.size
        max_resolution = 2000
        if width > max_resolution or height > max_resolution:
            raise ValidationError(
                f"Разрешение изображения не должно превышать {max_resolution}px по ширине или высоте.",
                code='resolution_too_large'
            )
    except Image.UnidentifiedImageError:
        raise ValidationError("Загруженный файл не является поддерживаемым изображением.", code='invalid_image')
    except Exception as e:
        raise ValidationError(f"Ошибка при обработке изображения: {e}", code='processing_error')

class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Выберите название категории")

    def __str__(self):
        return self.name


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Пользователь"
    )

    title = models.CharField(max_length=200, verbose_name="Напишите заголовок к заявке")
    description = models.TextField(verbose_name="Напишите к заявке описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Выберите категорию заявки")
    image = models.FileField(
        upload_to='application',
        validators=[validate_image],
        verbose_name="Загрузите фото заявки"
    )
    design_image = models.ImageField(
        upload_to='admin',
        blank=True,
        null=True,
        verbose_name="Изображение дизайна"
    )
    LOAN_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('s', 'Выполнено'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='n', verbose_name='Статус заявки',help_text='Статус заявки')
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания заявки")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('application-detail', args=[str(self.id)])

    def display_category(self):
        return self.category.name if self.category else "Без категории"
    display_category.short_description = 'Category'


