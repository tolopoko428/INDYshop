from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# Model for User
class User(AbstractUser):
    login = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=100, null=False)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.login

