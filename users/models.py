from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.utils.translation import gettext_lazy as _
from store.models import City, WareHouse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise DRFValidationError({'email': _('Поле электронной почты должно быть заполнено')})

        try:
            validate_email(email)
        except DjangoValidationError:
            raise DRFValidationError({'email': _('Неправильный формат электронной почты')})

        if self.model.objects.filter(email=email).exists():
            raise DRFValidationError({'email': _('Электронная почта уже используется')})

        if password:
            try:
                validate_password(password)
            except DjangoValidationError as e:
                raise DRFValidationError({'password': _('Пароль не соответствует требованиям: ') + ', '.join(e.messages)})
        else:
            raise DRFValidationError({'password': _('Пароль не может быть пустым')})

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrator')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    ROLE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
        ('admin', 'Администратор'),
    )
    username = None
    email = models.EmailField(blank=False, max_length=255, unique=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer', verbose_name="Роль")
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name='Город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'role']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=['email'], name='customuser_email_idx'),
            models.Index(fields=['role'], name='customuser_role_idx'),
        ]


class CustomerDeliverWareHouse(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "buyer"},
        verbose_name="Покупатель"
    )
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, blank=False, verbose_name="Склад")

    def __str__(self):
        return f'{self.user.email} {self.warehouse}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.user.city != self.warehouse.store_city.city:
            raise ValidationError("Склад должен находиться в том же городе, что и покупатель")

    class Meta:
        verbose_name = "Адрес Склада Покупателя"
        verbose_name_plural = "Адресы Складов Покупателей"
        indexes = [
            models.Index(fields=['user'], name='customer_user_idx'),
            models.Index(fields=['warehouse'], name='customer_warehouse_idx'),
        ]
