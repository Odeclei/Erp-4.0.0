import logging

from getmac import get_mac_address as gma

from rule.models import MacId, Turno
from site_setup.models import Category, SiteSetup

# print(gma())

logger = logging.getLogger("site_setup")


# def log_mac_address(request):
#     try:
#         mac_address = gma()
#         logger.info(f"MAC Address: {mac_address}")
#     except Exception as e:
#         logger.error(f"Erro ao obter o MAC Address: {e}")

#     user = request.user
#     if user.is_authenticated:
#         logger.info(f"Usuário autenticado: {user.username}")
#     else:
#         logger.warning("Usuário não autenticado")
#     return


def site_setup(request):
    setup = SiteSetup.objects.order_by("-id").first()
    category = Category.objects.all()

    try:
        mac_address = gma()
        logger.info(f"MAC Address: {mac_address}")
        if mac_address:
            try:
                mac = MacId.objects.get(mac_id=mac_address)
            except MacId.DoesNotExist:
                mac = MacId.objects.create(mac_id=mac_address)
    except Exception as e:
        logger.error(f"Erro ao obter o MAC Address: {e}")

    user = request.user
    if user.is_authenticated:
        logger.info(f"Usuário autenticado: {user.username}")
    else:
        logger.warning("Usuário não autenticado")

    # try:
    #     mac = MacId.objects.get(mac_id=mac_address)
    # except MacId.DoesNotExist:

    #     mac = MacId.objects.create(mac_id=mac_address)

    return {
        "site_setup": setup,
        "category": category,
        # "mac_id": mac,
    }


def horario_turnos(request):
    try:
        # Tenta encontrar o turno
        turno = Turno.objects.get(name="Comercial")

        # Se o turno for encontrado, retorna os valores
        return {
            "hr_inicio_turno": turno.hora_inicio,
            "hr_inicio_almoco": turno.hora_inicio_almoco,
            "hr_fim_almoco": turno.hora_fim_almoco,
        }
    except Turno.DoesNotExist:
        # Se o turno não for encontrado, retorna valores padrão
        return {
            "hr_inicio_turno": "00:00:00",
            "hr_inicio_almoco": "00:00:00",
            "hr_fim_almoco": "00:00:00",
        }
