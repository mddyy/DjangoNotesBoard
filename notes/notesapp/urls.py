from django.urls import path, include
from .views import *


urlpatterns = [
    path('', MainPage.as_view(), name='mainpage'),
    path('archive/', ArchivePage.as_view(), name='archive'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'^note/(?P<pk>[-\w]+)/$', edit_note, name='edit'),
]