from django.urls import path
from pedidos.views import (
    PedidoListView,
    PedidoCreateView,
    PedidoDetailView,
    PedidoUpdateView,
    PedidoDeleteView,
    PedidoSearchView,
    ItemPedidoCreateView,
    ItemPedidoDeleteView,
    ItemPedidoUpdateView,
    EndPedidoView,
    LiberarPedido,
    ImprimeEtiquetas,
    ImportarPedidoView,
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
    path("<int:pk>/add_item/", ItemPedidoCreateView.as_view(), name="add_item"),
    path("<int:pk>/delete_item/", ItemPedidoDeleteView.as_view(), name="delete_item"),
    path(
        "<int:pk>/<str:pedido_number>/update-item/",
        ItemPedidoUpdateView.as_view(),
        name="update_item",
    ),
    path("<int:pk>/finalizar_edicao/", EndPedidoView, name="finalizar_edicao"),
    path("<int:pk>/liberar_pedido/", LiberarPedido, name="liberar_pedido"),
    path("<int:pk>/imprime_etiquetas/", ImprimeEtiquetas, name="imprimir_etiquetas"),
    path("importar_pedido/", ImportarPedidoView.as_view(), name="importar_pedido"),
    # path(
    #     "<int:pk>/<int:order_number>/delete_item/",
    #     ItemPedidoDeleteView.as_view(),
    #     name="delete_item",
    # ),
]
