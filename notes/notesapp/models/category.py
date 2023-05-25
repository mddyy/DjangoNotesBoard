from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Категория заметки. Пока нет возможности их создавать кроме как через админку
    """
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name