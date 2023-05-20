from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from .models import Category, Note, Archive
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPage(LoginRequiredMixin, TemplateView):
    template_name = 'notesapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        notes = Note.objects.filter(creator=self.request.user)

        context.update(
            {
                'notes': notes,
            }
        )
        return context
