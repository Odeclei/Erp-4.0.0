# /home/james/mrp4.0app/middleware/session_timeout.py

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
import time


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.session_timeout = settings.SESSION_COOKIE_AGE

    def __call__(self, request):
        # Ignorar páginas de login/logout para evitar loops de redirecionamento
        if not request.path.startswith(settings.LOGIN_URL):
            # if not request.path.startswith(settings.LOGIN_URL) and not request.path.startswith(settings.LOGOUT_URL):
            if request.user.is_authenticated:
                last_activity = request.session.get("last_activity")

                if last_activity:
                    if time.time() - last_activity > self.session_timeout:
                        logout(request)
                        return redirect(settings.LOGIN_URL)

                request.session["last_activity"] = time.time()

        response = self.get_response(request)
        return response
