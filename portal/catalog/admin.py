from django.contrib import admin
from unicodedata import category

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
        exclude = ['image']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        previous_status = self.instance.status if self.instance else None

        # Проверка изменения статуса
        if previous_status in ['a', 's'] and status != previous_status:
            raise ValidationError("Нельзя менять статус после 'Принято в работу' или 'Выполнено'.")

        # Если статус меняется на 'Принято в работу', проверяем комментарий
        if status == 'a' and not cleaned_data.get('comment'):
            raise ValidationError("Пожалуйста, добавьте комментарий при смене статуса на 'Принято в работу'.")

        # Если статус меняется на 'Выполнено', проверяем изображение дизайна
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Если объект существует, проверяем его статус
        if obj:
            status = obj.status

            # Если статус 'Принято в работу', удаляем поле 'design_image'
            if status == 'a':
                if 'design_image' in form.base_fields:
                    form.base_fields['design_image'].required = False
                    del form.base_fields['design_image']

            # Если статус 'Выполнено', удаляем поле 'comment'
            elif status == 's':
                if 'comment' in form.base_fields:
                    form.base_fields['comment'].required = False
                    del form.base_fields['comment']

        return form

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.comment = form.cleaned_data.get('comment', '')
            obj.design_image = form.cleaned_data.get('design_image', None)
            with transaction.atomic():
                obj.save()

admin.site.register(Category)

