from django.urls import path, include
from .views import MainPage, ArchivePage


urlpatterns = [
    path('', MainPage.as_view(), name='mainpage'),
    path('archive/', ArchivePage.as_view(), name='archive'),
    path('accounts/', include('django.contrib.auth.urls')),
]