from django.urls import path
from pedidos.views import (
    PedidoListView,
    PedidoCreateView,
    PedidoDetailView,
    PedidoUpdateView,
    PedidoDeleteView,
    PedidoSearchView,
    ItemPedidoCreateView,
    ItemPedidoUpdateView,
)

app_name = "pedidos"


urlpatterns = [
    # crud Pedidos
    path("", PedidoListView.as_view(), name="index"),
    path("create/", PedidoCreateView.as_view(), name="create"),
    path("<int:pk>/detail/", PedidoDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", PedidoUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", PedidoDeleteView.as_view(), name="delete"),
    path("busca/", PedidoSearchView.as_view(), name="search"),
    # add item pedido
    path("<int:pk>/add-item/", ItemPedidoCreateView.as_view(), name="add_item"),
    path(
        "<int:pk>/<str:pedido_number>/update-item/",
        ItemPedidoUpdateView.as_view(),
        name="update_item",
    ),
    # path(
    #     "<int:pk>/<int:order_number>/delete_item/",
    #     ItemPedidoDeleteView.as_view(),
    #     name="delete_item",
    # ),
]
