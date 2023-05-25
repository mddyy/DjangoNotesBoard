from django.db import models
from django.utils import timezone
from .note import Note


class Archive(models.Model):
    """
    Запись об архивации заметки
    """
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    archivation_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.note)