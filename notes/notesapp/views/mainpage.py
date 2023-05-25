from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from .note_forms import get_user_notes


class MainPage(LoginRequiredMixin, TemplateView):
    """
    Представление главной страницы
    """
    template_name = 'notesapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        notes = get_user_notes(self.request)

        # передать полученный список в шаблон
        context.update(
            {
                'notes': notes,
            }
        )

        return context