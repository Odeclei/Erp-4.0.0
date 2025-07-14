# flake8: noqa
from django.contrib.auth import views as auth_views
from django.urls import include, path

from site_setup import views

app_name = 'site_setup'

urlpatterns = [
    path('', views.index, name="index"),
    # path('login/', auth_views.LoginView.as_view(template_name='site_setup/Login.html'), name='login'),
    path('login/', views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home_view, name='home'),
]
