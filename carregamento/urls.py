from django.urls import path
from carregamento.views import (
    CarregamentoCreateView,
    CarregamentoDetailView,
    CarregamentoListView,
    CarregamentoSearchView,
    ler_cod_barras,
    # salvar_itens,
    encerrarCarregamento,
)

app_name = "carregamento"


urlpatterns = [
    # crud Pedidos
    path("", CarregamentoListView.as_view(), name="index"),
    path("create/", CarregamentoCreateView.as_view(), name="carga_create"),
    path("<int:pk>/create/", CarregamentoCreateView.as_view(), name="carga_create_pk"),
    path("<int:pk>/detail/", CarregamentoDetailView.as_view(), name="carga_detail"),
    path("search/", CarregamentoSearchView.as_view(), name="search"),
    # funções ajax
    # path("salvar_itens/", salvar_itens, name="salvar_itens"),
    path("barcode/", ler_cod_barras, name="ler_codigo_barras"),
    path("finish/", encerrarCarregamento, name="encerrar_carregamento"),
]
