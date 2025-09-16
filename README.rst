# SISTEMA DE APONTAMENTO DE PRODUÇÃO

## Passo a Passo para utilização após instalação do conjunto:


Executar os seguintes comandos:
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
 - nome do usuário
 - email do usuário
 - senha e confirmação de senha (em produção, SEMPRE utiizar senha forte!)


acessar área administrativa:
    (seu ip ou dominio)/admin e logar;

## CONFIGURAÇÕES INICIAIS
1. AUTENTICAÇÃO E AUTORIZAÇÃO
    **Usuário**: completar o cadastro do superuser.



2. SITE_SETUP
   **obrigatório:**

    Tìtulo da Página
    Descrição

    **Favicon**: imagem png 32x32px - aparece canto superior do navegador.
    **LogoSite**: imagem png para header da pagina.

3. RULE
    **obrigatório**

    **Empresas**: cadastrar dados da instituição.
    **Grupos**: cadastrar dados da instituição.
    **Setores**: cadastrar dados da instituição.
    **Postos de Trabalho**: cadastrar dados da instituição.
    **Máquinas**: cadastrar dados da instituição.
    **Turnos**: cadastrar dados da instituição.
    **Mac ids**: cadastro dos macs e relacionamentos com posto de trabalho (maquina)
