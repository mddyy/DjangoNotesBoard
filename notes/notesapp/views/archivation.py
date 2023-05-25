from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from ..models.note import Note
from ..models.archive import Archive
from django.shortcuts import redirect, get_object_or_404


class ArchivePage(LoginRequiredMixin, TemplateView):
    template_name = 'notesapp/archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivePage, self).get_context_data(**kwargs)

        # отобрать все заметки данного пользователя за исключением архивированных
        archive = {item.note for item in Archive.objects.all()}
        archive_count = len(archive)
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
                'archive_count': archive_count
            }
        )
        return context


def archivate_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)
    if not Archive.objects.filter(note_id=note_instance.id).exists():
        Archive.objects.create(note=note_instance)
    return redirect('mainpage')


def unarchivate_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)
    if Archive.objects.filter(note_id=note_instance.id).exists():
        Archive.objects.get(note_id=note_instance.id).delete()
    return redirect('mainpage')


def delete_note(request, pk):
    note_instance = get_object_or_404(Note, pk=pk)
    if Archive.objects.filter(note_id=note_instance.id).exists():
        Archive.objects.get(note_id=note_instance.id).delete()
        Note.objects.get(id=note_instance.id).delete()
    return redirect('archive')


def clear_archive(request):
    for item in Archive.objects.all():
        Note.objects.filter(id=item.note.id).delete()
    return redirect('mainpage')