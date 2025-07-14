from django.urls import path
from carregamento import views

app_name = 'carregamento'


urlpatterns = [
    path("", views.index, name='index'),
]
