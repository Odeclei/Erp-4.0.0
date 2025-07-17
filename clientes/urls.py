from django.urls import path

from clientes.views import (
    ClienteReadView,
    ClienteCreateView,
    ClienteDetailView,
    ClienteUpdateView,
    ClienteDeleteView,
    ClienteBuscaView,
)

app_name = "clientes"


urlpatterns = [
    path("create/", ClienteCreateView.as_view(), name="create"),
    path("", ClienteReadView.as_view(), name="read"),
    path("<int:pk>/detail/", ClienteDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", ClienteUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ClienteDeleteView.as_view(), name="delete"),
    path("busca/", ClienteBuscaView.as_view(), name="busca"),
]
