from django.urls import path
from desempenho import views

app_name = "desempenho"

urlpatterns = [
    # Dashboard
    path("dashboard/", views.DashboardOEEView.as_view(), name="dashboard"),
    
    # APIs
    path("api/hoje/", views.APIDesempenhoHojeView.as_view(), name="api_hoje"),
    path("api/maquina/<int:machine_id>/", views.APIDesempenhoMaquinaView.as_view(), name="api_maquina"),
    path("api/setor/<int:setor_id>/", views.APIDesempenhoSetorView.as_view(), name="api_setor"),
    path("api/grupo/<int:grupo_id>/", views.APIDesempenhoGrupoView.as_view(), name="api_grupo"),
]
