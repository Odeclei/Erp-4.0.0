# flake8: noqa
from django.urls import path
from .views import (
    ItemAcabadoListView,
    ItemAcabadoSearchView,
    ItemAcabadoDetailView,
    ItemAcabadoCreateView,
    GetBomAbaView,
    AddEstruturaProdView,
    RemoveEstruturaProdView,
    AddComponenteCompraView,
    RemoveComponenteCompraView,
    BuscaItemBaseView,
    BuscaComponenteView,
)

app_name = "_itens"

urlpatterns = [
    # urls progamação
    path("", ItemAcabadoListView.as_view(), name="item_list"),  # Lista todas as ordens
    path("busca/", ItemAcabadoSearchView.as_view(), name="item_search"),
    path("<int:pk>/detail/", ItemAcabadoDetailView.as_view(), name="item_detail"),
    path("create/", ItemAcabadoCreateView.as_view(), name="item_create"),
    # API AJAX para gerenciar BOM
    path("<int:item_id>/bom/get/", GetBomAbaView.as_view(), name="bom_get"),
    path(
        "<int:item_id>/bom/add-estrutura/",
        AddEstruturaProdView.as_view(),
        name="bom_add_estrutura",
    ),
    path(
        "bom/remove-estrutura/<int:estructura_id>/",
        RemoveEstruturaProdView.as_view(),
        name="bom_remove_estrutura",
    ),
    path(
        "<int:item_id>/bom/add-componente/",
        AddComponenteCompraView.as_view(),
        name="bom_add_componente",
    ),
    path(
        "bom/remove-componente/<int:componente_prog_id>/",
        RemoveComponenteCompraView.as_view(),
        name="bom_remove_componente",
    ),
    # Autocomplete para busca de itens
    path("api/busca-itembase/", BuscaItemBaseView.as_view(), name="busca_itembase"),
    path(
        "api/busca-componente/", BuscaComponenteView.as_view(), name="busca_componente"
    ),
]
