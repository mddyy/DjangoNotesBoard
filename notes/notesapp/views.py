from django import forms
from django.views.generic.base import TemplateView, View
from .models import Category, Note, Archive
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
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
                        .order_by('-last_change') if note not in archive
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
                        .order_by('-last_change') if note in archive
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


class NoteForm(LoginRequiredMixin, forms.ModelForm, View):
    class Meta:
        model = Note
        fields = ('title', 'text', 'category', 'color')
        widgets = {
            "color": forms.RadioSelect(attrs={"background-color": Note.COLOR_CHOICES[1]}),
        }
        labels = {
            "title": "",
            "text": "",
            "color": ""
        }


def new_note(request):
    form = NoteForm()

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
        general_category = Category.objects.all()[0]
        form = NoteForm(initial={'category': general_category, 'color': Note.COLOR_CHOICES[0]})

    return render(request, 'notesapp/edit.html', {'form': form})


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


def archivate_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)
    Archive.objects.create(note=note_instance)
    return redirect('mainpage')


def unarchivate_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)
    Archive.objects.filter(note=note_instance)[0].delete()
    return redirect('mainpage')


def delete_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)
    if Archive.groups.filter(Note=note_instance).exists():
        Archive.objects.get(note=note_instance).delete()
        Note.objects.get(note=note_instance).delete()
    return redirect('archive')


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_confirm']

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            "password": forms.PasswordInput(),
        }


def register(request):
    # если запрос был POST - создать шаблон с заполненными данными
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password'])
            new_user.group = Group.objects.filter(name='common user')[0]
            new_user.save()
            return redirect('mainpage')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
