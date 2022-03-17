from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE = [
        ('admin', 'admin'),
        ('user', 'user'),
    ]

class User(AbstractUser):
    # унаследовали user из django и добавили немного своего
    
    user_permission = models.CharField(choices=USER_TYPE, max_length=100, default = 'user')
    # avatar = models.ImageField()
    phone_number = models.IntegerField(null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
