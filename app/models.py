from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class CustomUser(AbstractUser):
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE,null=True)
    email = models.EmailField(unique=True)
