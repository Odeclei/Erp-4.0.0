from django.urls import path
from .views import (
    index,
    get_grupos,
    get_setores_by_grupo,
    cadastrar_posto,
    GrupoListView,
    GroupCreateView,
    GrupoUpdateView,
    SetorListView,
    SetorUpdateView,
    SetorCreateView,
    PostoTrabaloListView,
    PostoTrabalhoUpdateView,
    PostoTrabalhoCreateView,
)


app_name = "rule"

urlpatterns = [
    path("", index, name="index"),
    path("api/grupos/", get_grupos, name="api_get_grupo"),
    path(
        "api/grupos/<int:grupo_id>/setores/",
        get_setores_by_grupo,
        name="api_setores_by_grupo",
    ),
    path("api/cadastrar_posto/", cadastrar_posto, name="api_cadastrar_posto"),
    # urls para Grupos
    path("grupos/", GrupoListView.as_view(), name="grupos_list"),
    path("grupos/create/", GroupCreateView.as_view(), name="grupos_create"),
    path("grupos/<int:pk>/update/", GrupoUpdateView.as_view(), name="grupos_update"),
    # urls para Setor
    path("setores/", SetorListView.as_view(), name="setores_list"),
    path("setores/<int:pk>/update/", SetorUpdateView.as_view(), name="setores_update"),
    path("setores/create/", SetorCreateView.as_view(), name="setores_create"),
    # urls para posto de trabalho
    path("postos/", PostoTrabaloListView.as_view(), name="postos_list"),
    path(
        "postos/<int:pk>/update/",
        PostoTrabalhoUpdateView.as_view(),
        name="postos_update",
    ),
    path("postos/create/", PostoTrabalhoCreateView.as_view(), name="postos_create"),
]
