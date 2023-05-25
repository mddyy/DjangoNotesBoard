from django.urls import path, include
from .views.archivation import *
from .views.mainpage import MainPage
from .views.register import register
from .views.note_forms import *
from .views.category_form import *


urlpatterns = [
    path('', MainPage.as_view(), name='mainpage'),
    path('archive/', ArchivePage.as_view(), name='archive'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('note/<int:pk>/', edit_note, name='edit'),
    path('note/new/', new_note, name='new'),
    path('note/<int:pk>/archivate/', archivate_note, name='archivate'),
    path('note/<int:pk>/unarchivate/', unarchivate_note, name='unarchivate'),
    path('note/<int:pk>/delete/', delete_note, name='delete'),
    path('register/', register, name='register'),
    path('clear_archive/', clear_archive, name='clear_archive'),
    path('category/new/', new_category, name='new_category'),
    path('category/<int:pk>/delete/', delete_category, name='delete_category')
]
