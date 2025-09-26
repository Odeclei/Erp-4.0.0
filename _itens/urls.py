# flake8: noqa
from django.urls import path
from .views import (
    ItemAcabadoListView,
    ItemAcabadoSearchView,
    ItemAcabadoDetailView,
    ItemAcabadoCreateView,
)

app_name = "_itens"

urlpatterns = [
    # urls progamação
    path("", ItemAcabadoListView.as_view(), name="item_list"),  # Lista todas as ordens
    path("busca/", ItemAcabadoSearchView.as_view(), name="item_search"),
    path("<int:pk>/detail/", ItemAcabadoDetailView.as_view(), name="item_detail"),
    path("create/", ItemAcabadoCreateView.as_view(), name="item_create"),
]
