from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from .models import Category, Note
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPage(LoginRequiredMixin, TemplateView):
    template_name = 'notesapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        categories = (note.category for note in Note.objects.filter(creator=self.request.user))

        notes = [
            {
                'category': category,
                'notes_of_category': [note for note in Note.objects.filter(creator=self.request.user, category=category).order_by('last_change')]
            }
            for category in categories
        ]

        context.update(
            {
                'notes': notes,
            }
        )
        return context
