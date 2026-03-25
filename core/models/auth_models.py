from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

class CustomUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(
            username=username,
            password=password,
            **extra_fields
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, username,  password=None,  **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=56)
    username = models.CharField(unique=True, max_length=56)
    email = models.EmailField()
    age = models.SmallIntegerField(default=18)
    gender = models.BooleanField(choices=[
        (True, "Erkak"),
        (False, "Ayol")
    ],null=True, blank=True)

    role = models.SmallIntegerField(choices=[
        (1, 'Admin'),
        (2, "seller"),
        (3, 'Buyer'),
    ], default=3, help_text="Admin(1), Seller(2), Buyer(3)", editable=False)

    password = models.CharField(max_length=56)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["role", ]

    def response(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "gender": self.gender,
            "role": self.role,
            "password": self.password,
            "is_active": "ha active" if self.is_active else "user ban qilingan",
            "is_staff": 'ha staff' if self.is_staff else "yo'q",
            "is_superuser": "ha superuser" if self.is_superuser else "yo'q"
        }


class Firma(models.Model):
    name = models.CharField("onlayn magazin, nomi", max_length=56)
    logo = models.ImageField(upload_to="brands/")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
        "role": 2
    })

class VerifivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"code for - {self.user.username}"


