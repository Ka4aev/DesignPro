from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from .models import User


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=254,
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё -]+$',
                message="Имя должно содержать только кириллические буквы, дефисы и пробелы."
            )
        ]
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=254,
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё -]+$',
                message="Фамилия должна содержать только кириллические буквы, дефисы и пробелы."
            )
        ]
    )
    patronymic = forms.CharField(
        label="Отчество",
        max_length=254,
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё -]+$',
                message="Отчество должно содержать только кириллические буквы, дефисы и пробелы."
            )
        ]
    )
    username = forms.CharField(
        label="Логин",
        max_length=254,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9-]+$',
                message="Логин должен содержать только латиницу и дефисы."
            )
        ]
    )
    email = forms.EmailField(
        label="Почта",
        max_length=254,
        validators=[EmailValidator(message="Введите действительный email-адрес.")]
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput
    )
    consent = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        initial=True,
        error_messages={"required": "Необходимо согласие на обработку персональных данных."}
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Логин уже занят.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Почта уже занята.")
        return email

    def clean(self):
        super().clean()

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Пароли должны совпадать.")

        return self.cleaned_data

    def save(self, commit=True):
        new_user = super().save(commit=False)
        new_user.set_password(self.cleaned_data.get("password"))
        if commit:
            new_user.save()
        return new_user

    class Meta:
        model = User
        fields = ("last_name","first_name","patronymic", "username", "email")
