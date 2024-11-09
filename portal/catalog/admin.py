from django.contrib import admin
from .models import Category, Application
from django.core.exceptions import ValidationError
from django import forms
from django.db import transaction

class ApplicationAdminForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Комментарий (обязателен при смене статуса на 'Принято в работу')"
    )
    design_image = forms.ImageField(
        required=False,
        label="Изображение дизайна (обязательно при смене статуса на 'Выполнено')"
    )

    class Meta:
        model = Application
        fields = '__all__'
        exclude = ['image']  # Исключаем поле 'image' из формы

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        previous_status = self.instance.status if self.instance else None

        # Проверка изменения статуса
        if previous_status in ['a', 's'] and status != previous_status:
            raise ValidationError("Нельзя менять статус после 'Принято в работу' или 'Выполнено'.")

        # Если статус меняется на 'Принято в работу'
        if status == 'a' and not cleaned_data.get('comment'):
            raise ValidationError("Пожалуйста, добавьте комментарий при смене статуса на 'Принято в работу'.")

        # Если статус меняется на 'Выполнено'
        if status == 's' and not cleaned_data.get('design_image'):
            raise ValidationError("Пожалуйста, загрузите изображение дизайна при смене статуса на 'Выполнено'.")

        return cleaned_data


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    list_display = ('title', 'user', 'status', 'created_at', 'category')
    readonly_fields = ('user', 'title', 'description', 'category', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'user__username', 'description')
    exclude = ['image']



    def save_model(self, request, obj, form, change):
        if form.is_valid():
            with transaction.atomic():
                obj.save()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def delete_model(self, request, obj):
        # Удалить все заявки, связанные с категорией
        Application.objects.filter(category=obj).delete()
        obj.delete()
