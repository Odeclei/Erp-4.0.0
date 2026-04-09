# flake8: noqa
from django.urls import path

from ppcp.views import (
    BuscaItemView,
    GetBomView,
    ItemOrderCreateView,
    ItemOrderDeleteView,
    ItemOrderUpdateView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderSearchView,
    OrderUpdateView,
    SubItemDeleteView,
    SubItemOrderUpdateView,
    a_quantidade,
    c_quantidade,
)

app_name = "order"

urlpatterns = [
    # urls progamação
    path("", OrderListView.as_view(), name="list"),  # Lista todas as ordens
    path(
        "create/", OrderCreateView.as_view(), name="create"
    ),  # Cria novas ordens de produção
    path(
        "<int:pk>/detail/", OrderDetailView.as_view(), name="detail"
    ),  # Detalha ordem de produção Selecionada
    path(
        "buscaitem/", BuscaItemView.as_view(), name="busca_item"
    ),  # busca item para adicionar na ordem de produção
    path("getbom/", GetBomView.as_view(), name="get_bom"),  # retorna BOM de um item
    path(
        "<int:pk>/update/", OrderUpdateView.as_view(), name="update"
    ),  # Atualiza ordem de produção selecionada
    path(
        "search/", OrderSearchView.as_view(), name="search"
    ),  # Busca ordens de produção
    # add item programação
    path("<int:pk>/add-item/", ItemOrderCreateView.as_view(), name="add_item"),
    path(
        "<int:pk>/<str:order_number>/update-item/",
        ItemOrderUpdateView.as_view(),
        name="update_item",
    ),
    path(
        "<int:pk>/update-subitem/",
        SubItemOrderUpdateView.as_view(),
        name="update_subitem",
    ),
    path(
        "<int:pk>/<str:order_number>/delete_item/",
        ItemOrderDeleteView.as_view(),
        name="delete_item",
    ),
    path("<int:pk>/delete/", SubItemDeleteView.as_view(), name="delete"),
    path("quantidade/", c_quantidade, name="quantidade"),
    path("alterqtde/", a_quantidade, name="alterqtde"),
]
