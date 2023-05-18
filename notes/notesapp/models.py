from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    COLOR_CHOICES = [
        ('#FFFFFF', 'White'),
        ('#FFFF99', 'Yellow'),
        ('#CCFF33', 'Green'),
        ('#66CCFF', 'Blue'),
        ('#FF9933', 'Orange')
    ]
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default=COLOR_CHOICES[0])


class Note(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


class Archive(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    archivation_date = models.DateField(default=date.today())

    @staticmethod
    def archivate(note: Note):
        return Archive(note_id = note.id, archivation_date = date.today())