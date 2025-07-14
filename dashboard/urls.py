from django.urls import path

from .views import initial

app_name = 'dashboard'

urlpatterns = [
    path('', initial, name='index'),
]
