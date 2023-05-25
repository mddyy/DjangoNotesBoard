from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .category import Category


class Note(models.Model):
    COLOR_CHOICES = [
        ('#FFFFFF', 'White'),
        ('#FFFF99', 'Yellow'),
        ('#CCFF33', 'Green'),
        ('#66CCFF', 'Blue'),
        ('#FF9933', 'Orange')
    ]

    title = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    last_change = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default=COLOR_CHOICES[0])

    def __str__(self):
        return self.title

    @property
    def sliced_text(self):
        if len(self.text) > 80:
            return self.text[:80] + '...'
        else:
            return self.text


