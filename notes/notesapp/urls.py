from django.urls import path, include
from .views import MainPage


urlpatterns = [
    path('', MainPage.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
]