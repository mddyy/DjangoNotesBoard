from django.contrib import admin
from .models.archive import Archive
from .models.note import Note
from .models.category import Category

admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Archive)
