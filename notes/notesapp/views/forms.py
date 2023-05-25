from django import forms
from django.views.generic.base import TemplateView, View
from ..models.note import Note
from ..models.archive import Archive
from ..models.category import Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone


class NoteForm(LoginRequiredMixin, forms.ModelForm, View):
    class Meta:
        model = Note
        fields = ('title', 'text', 'category', 'color')
        labels = {
            "title": "",
            "text": "",
            "color": ""
        }


def get_user_notes(request, archivated=False):
    # отобрать все заметки данного пользователя за исключением архивированных
    archive = {item.note for item in Archive.objects.all()}
    categories = {note.category for note in Note.objects.filter(creator=request.user) if note not in archive}

    if archivated:
    # сгруппировать заметки по категориям и отсортировать по дате изменения
        notes = [
            {
                'category': category,
                'notes_of_category': [
                    note for note in Note.objects \
                        .filter(creator=request.user, category=category) \
                        .order_by('-last_change') if note not in archive
                ]
            }
            for category in categories
        ]
    else:
        notes = [
            {
                'category': category,
                'notes_of_category': [
                    note for note in Note.objects \
                        .filter(creator=request.user, category=category) \
                        .order_by('-last_change') if note in archive
                ]
            }
            for category in categories
        ]

    return notes


def new_note(request):
    init_color = Note.COLOR_CHOICES[0][1]
    init_category = Category.objects.all()[0]
    form = NoteForm()

    # отобрать все заметки данного пользователя за исключением архивированных
    archive = {item.note for item in Archive.objects.all()}
    categories = {note.category for note in Note.objects.filter(creator=request.user) if note not in archive}

    # сгруппировать заметки по категориям и отсортировать по дате изменения
    notes = [
        {
            'category': category,
            'notes_of_category': [
                note for note in Note.objects \
                    .filter(creator=request.user, category=category) \
                    .order_by('-last_change') if note not in archive
            ]
        }
        for category in categories
    ]

    # если запрос был POST - создать шаблон с заполненными данными
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note_instance = form.save(commit=False)
            note_instance.creator = request.user
            note_instance.last_change = timezone.now()

            note_instance.title = form.cleaned_data['title']
            note_instance.text = form.cleaned_data['text']
            note_instance.category = form.cleaned_data['category']
            note_instance.color = form.cleaned_data['color']

            note_instance.save()
            return redirect('mainpage')

    else:
        form = NoteForm(initial={
            'form': form,
            'notes': notes,
            'color': init_color,
            'category': init_category
        })

    return render(request, 'notesapp/new.html', {'form': form, 'notes': notes})


def edit_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)

    # отобрать все заметки данного пользователя за исключением архивированных
    archive = {item.note for item in Archive.objects.all()}
    categories = {note.category for note in Note.objects.filter(creator=request.user) if note not in archive}

    # сгруппировать заметки по категориям и отсортировать по дате изменения
    notes = [
        {
            'category': category,
            'notes_of_category': [
                note for note in Note.objects \
                    .filter(creator=request.user, category=category) \
                    .order_by('-last_change') if note not in archive
            ]
        }
        for category in categories
    ]

    # если запрос был POST - создать шаблон с заполненными данными
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note_instance)

        if form.is_valid():
            note_instance = form.save(commit=False)
            note_instance.creator = request.user
            note_instance.last_change = timezone.now()

            note_instance.title = form.cleaned_data['title']
            note_instance.text = form.cleaned_data['text']
            note_instance.category = form.cleaned_data['category']
            note_instance.color = form.cleaned_data['color']

            note_instance.save()
            return redirect('mainpage')

    else:
        form = NoteForm(instance=note_instance)

    return render(request, 'notesapp/edit.html', {'form': form, 'notes': notes, 'note_color': note_instance.color})