from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.


def index(request):
    return render(
        request,
        'site_setup/index.html'
    )


def login_view(request):  
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Realiza o login

            # Lógica de redirecionamento (incluindo o parâmetro 'next')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                # Redireciona para o URL padrão após login
                return redirect(settings.LOGIN_REDIRECT_URL)

        else:
            # Você pode inspecionar form.errors aqui para depurar o porquê
            pass  # O template irá renderizar os erros do formulário
    else:  # GET request
        form = AuthenticationForm()

    # Passa o parâmetro 'next' do GET para o template, se existir
    next_param = request.GET.get('next', '')

    # Define a ação do formulário usando reverse()
    # Certifique-se de que 'site_setup:login' está configurado no seu urls.py
    form_action = reverse('site_setup:login')

    context = {
        'form': form,
        'next': next_param,  # Passa 'next' para o template
        'form_action': form_action,
    }

    return render(
        request,
        'site_setup/Login.html',
        context
    )

@login_required
def home_view(request):
    # Aqui você pode definir a lógica para a página inicial após o login
    return render(
        request,
        'site_setup/home.html'
    )
