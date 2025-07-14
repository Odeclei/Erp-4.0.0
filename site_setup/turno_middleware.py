# myapp/middleware.py
from django.utils.deprecation import MiddlewareMixin

from .context_processor import horario_turnos


class GlobalSettingsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.global_settings = horario_turnos
