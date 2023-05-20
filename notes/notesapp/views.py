from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from .models import Category, Note, Archive
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPage(LoginRequiredMixin, TemplateView):
    template_name = 'notesapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)

        # отобрать все заметки данного пользователя за исключением архивированных
        archive = {item.note for item in Archive.objects.all()}
        categories = {note.category for note in Note.objects.filter(creator=self.request.user) if note not in archive}

        # сгруппировать заметки по категориям и отсортировать по дате изменения
        notes = [
            {
                'category': category,
                'notes_of_category': [
                    note for note in Note.objects\
                        .filter(creator=self.request.user, category=category)\
                        .order_by('last_change')
                ]
            }
            for category in categories
        ]

        # передать полученный список в шаблон
        context.update(
            {
                'notes': notes,
            }
        )
        return context


class ArchivePage(LoginRequiredMixin, TemplateView):
    template_name = 'notesapp/archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivePage, self).get_context_data(**kwargs)

        # отобрать все заметки данного пользователя за исключением архивированных
        archive = {item.note for item in Archive.objects.all()}
        categories = {note.category for note in Note.objects.filter(creator=self.request.user) if note in archive}

        # сгруппировать заметки по категориям и отсортировать по дате изменения
        notes = [
            {
                'category': category,
                'notes_of_category': [
                    note for note in Note.objects\
                        .filter(creator=self.request.user, category=category)\
                        .order_by('last_change')
                ]
            }
            for category in categories
        ]

        # передать полученный список в шаблон
        context.update(
            {
                'notes': notes,
            }
        )
        return context
