from django.shortcuts import render


def main_page(request):
    return render(request, 'notesapp/main_page.html', {})
