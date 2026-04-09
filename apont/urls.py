from django.urls import path

from apont.views import (
    # get_template_url,
    ApontStop,
    FimProducaoView,
    IniciarSetupView,
    ReadBarcodeView,
    StopsMotiveView,
    SubgrupoStop,
)

app_name = "apont"

urlpatterns = [
    # path('', ReadBarcodeView, name='read_barcode'),
    path("", ReadBarcodeView, name="read_barcode"),
    path("start-setup/", IniciarSetupView, name="start_setup"),
    path("fim_producao/", FimProducaoView, name="fim_producao"),
    path("parada/", StopsMotiveView, name="stop_group"),
    path("subgrupo_stop/", SubgrupoStop, name="stop_subgroup"),
    path("apont_stop/", ApontStop, name="apont_stop"),
]
