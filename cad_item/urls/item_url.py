# flake8: noqa
from django.urls import path

from cad_item.views import (BuscaFamiliaView, BuscaSubitemView,
                            EstruturaDeleteView, FamilyCreateView,
                            FamilyProdView, FamilySearchView, FamilyUpdateView,
                            ItemCreateView, ItemDetailView,
                            ItemEstruturaCreateView, ItemListView,
                            ItemSearchView, ItemUpdateView, SubitemCreateView,
                            SubitemDetailView, SubitemSearchView,
                            SubitemUpdateView, SubItensView)
from cad_item.views.crud_item import EstruturaDeleteView

app_name = "cad_item"

urlpatterns = [
    path("", ItemListView.as_view(), name="read"),
    path("creat/", ItemCreateView.as_view(), name="creat"),
    path("<int:pk>/detail/", ItemDetailView.as_view(), name="detail"),
    path('buscafamilia', BuscaFamiliaView.as_view(), name='buscafamilia'),
    path("<int:pk>/update/", ItemUpdateView.as_view(), name="update"),
    path("search/", ItemSearchView.as_view(), name="search"),
    path('buscasubitem', BuscaSubitemView.as_view(), name='buscasubitem'),

    # ---------- urls Família Produto ---------------------
    path("<int:pk>/estr-create/", ItemEstruturaCreateView.as_view(), name="estrutura"),
    path("estrutura/<int:pk>/delete/", EstruturaDeleteView.as_view(), name="estrutura_delete"),
    # ---------- urls Família Produto ---------------------
    path("family/list/", FamilyProdView.as_view(), name="family_list"),
    path("family/create/", FamilyCreateView.as_view(), name="family_create"),
    path("family/<int:pk>/update/", FamilyUpdateView.as_view(), name="family_update"),
    path("family/search/", FamilySearchView.as_view(), name="family_search"),

    # ---------- urls Família Produto ---------------------
    path("subitens/list/", SubItensView.as_view(), name="subitem_list"),
    path("subitens/create/", SubitemCreateView.as_view(), name="subitem_create"),
    path("subitens/<int:pk>/", SubitemCreateView.as_view(), name="subitem_create"),
    path(
        "subitens/<int:pk>/detail/", SubitemDetailView.as_view(), name="subitem_detail"
    ),
    path(
        "subitens/<int:pk>/update/", SubitemUpdateView.as_view(), name="subitem_update"
    ),
    path("subitens/search/", SubitemSearchView.as_view(), name="subitem_search"),
]
