from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)


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
    last_change = models.DateTimeField(default=timezone.now())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default=COLOR_CHOICES[0])


class Archive(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    archivation_date = models.DateField(default=timezone.now().date())

    @staticmethod
    def archivate(note: Note):
        return Archive(note_id=note.id)