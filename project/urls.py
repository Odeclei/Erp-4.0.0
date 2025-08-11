from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("site_setup.urls")),
    path("apont/", include("apont.urls")),
    path("carregamento/", include("carregamento.urls")),
    path("clientes/", include("clientes.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("item/", include("cad_item.urls")),
    path("order/", include("ppcp.urls")),
    path("pedidos/", include("pedidos.urls")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
