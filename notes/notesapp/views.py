from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Category, Note, Archive


class MainPage(TemplateView):
    template_name = 'notesapp/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        #notes = Note.objects.all()

        """subjects = set()
        for note in notes:
            subject_name = score.subject.name
            subjects.add(subject_name)
            student_scores[score.student][subject_name] = score.value

        subjects = sorted(subjects)
        student_statistics = [
            {
                'student': student,
                'scores': [f'{scores[subject]:.1f}' for subject in subjects]
            }
            for student, scores in student_scores.items()
        ]
        context.update(
            {
                'subjects': subjects,
                'student_statistics': student_statistics
            }
        )"""
        return context
