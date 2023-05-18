from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Category, Note, Archive
from collections import defaultdict


class MainPage(TemplateView):
    template_name = 'notesapp/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        notes = Note.objects.all()

        context.update(
            {
                'notes': notes,
            }
        )
        return context
