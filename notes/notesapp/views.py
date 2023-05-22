from django import forms
from django.views.generic.base import TemplateView, View
from .models import Category, Note, Archive
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone


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
                        .order_by('last_change') if note not in archive
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
                        .order_by('last_change') if note in archive
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


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'category', 'color')


def edit_note(request, pk):
    form = NoteForm()
    note_instance = get_object_or_404(Note, pk=pk)
    note_instance.creator = request.user

    # если запрос был POST - создать шаблон с заполненными данными
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note_instance.title = form.cleaned_data['title']
            note_instance.category = form.cleaned_data['category']
            note_instance.color = form.cleaned_data['color']
            note_instance.last_change = timezone.now()
            note_instance.text = form.cleaned_data['text']

            note_instance.save()
            return HttpResponseRedirect(reverse('mainpage'))

    else:
        general_category = Category.objects.all()[0]
        form = NoteForm(initial={'category': general_category, 'color': Note.COLOR_CHOICES[0]})

    return render(request, 'notesapp/edit.html', {'form': form, 'note_instance': note_instance})


def new_note(request):
    pass
