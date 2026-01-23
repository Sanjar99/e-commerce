from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import UserManager  # mana shu file'ga qo'yasan

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be in the format: '+998xxxxxxxxx'."
)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    is_seller = models.BooleanField(default=False)

    # ✅ email bilan login
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # createsuperuser uchun
    objects = UserManager()

    def __str__(self):
        return self.email
