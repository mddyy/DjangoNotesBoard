from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from ..models.note import Note
from ..models.archive import Archive
from .forms import get_user_notes
from django.shortcuts import redirect, get_object_or_404


class ArchivePage(LoginRequiredMixin, TemplateView):
    template_name = 'notesapp/archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivePage, self).get_context_data(**kwargs)
        archive_count = len(Archive.objects.all())
        notes = get_user_notes(self.request, archivated=True)

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