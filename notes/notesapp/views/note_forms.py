from django import forms
from django.views.generic.base import View
from ..models.note import Note
from ..models.category import Category
from ..models.archive import Archive
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone


class NoteForm(LoginRequiredMixin, forms.ModelForm, View):
    """
    Форма добавления/редактирования заметки
    """
    class Meta:
        model = Note
        fields = ('title', 'text', 'category', 'color')
        labels = {
            "title": "",
            "text": "",
            "color": ""
        }


def get_user_notes(request, archivated=False):
    """
    Получить список заметок для отображения
    :param request:
    :param archivated: только архивированные (по умолчанию False)
    :return:
    """
    archive = {item.note for item in Archive.objects.all()}
    categories = Category.objects.filter(creator=request.user)
    if len(categories) == 0:
        Category.objects.create(creator=request.user, name='General')
        categories = Category.objects.all()

    if not archivated:
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
    """
    Создать новую заметку
    :param request:
    :return:
    """
    init_color = Note.COLOR_CHOICES[0][1]
    init_category = Category.objects.all()[0]
    form = NoteForm()
    notes = get_user_notes(request)

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
    """
    Редактировать существующую заметку
    :param request:
    :param pk:
    :return:
    """
    note_instance = get_object_or_404(Note, pk=pk)
    notes = get_user_notes(request)

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