from ..models.category import Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.views.generic.base import View
from django.shortcuts import render, redirect
from .note_forms import get_user_notes


class CategoryForm(LoginRequiredMixin, forms.ModelForm, View):
    """
    Форма добавления/редактирования категорий
    """

    class Meta:
        model = Category
        fields = ('name',)


def new_category(request):
    """
    Создать новую категорию
    :param request:
    :return:
    """
    form = CategoryForm()
    notes = get_user_notes(request)

    # если запрос был POST - создать шаблон с заполненными данными
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.creator = request.user

            new_cat.save()
            return redirect('mainpage')

    else:
        form = CategoryForm()

    return render(request, 'notesapp/new_category.html', {'form': form, 'notes': notes})