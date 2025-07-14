# flake8: noqa


import os
import sys
from pathlib import Path

import django
# import pandas as pd
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
# DJANGO_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False


django.setup()


if __name__ == '__main__':

    import csv

    from cad_item.models import Produtos

    def importar_csv_para_lista(arquivo_csv):
        lista_dados = []

        with open(arquivo_csv, 'r') as file:
            leitor_csv = csv.reader(file)
            for linha in leitor_csv:
                lista_dados.append(linha)
                # print(linha)

        return lista_dados

    arquivo_csv = r'utils\cadastro_produtos.csv'
    # arquivo_excel = r'utils\cadastro_sub_produtos.csv'
    lista_dados = importar_csv_para_lista(arquivo_csv)

    Produtos.objects.all().delete()

    django_add = []

    for item in lista_dados:
        lista = item

        # Separar cada elemento da lista pelo caractere ';'
        lista_separada = [elemento.split(';') for elemento in lista]

        # Achatar a lista de listas
        nova_lista = [item for sublist in lista_separada for item in sublist]

        refer = nova_lista[0]
        description = nova_lista[1]
        qtd_per_day = nova_lista[8]
        disc_prog = True
        disc_preparation = True
        disc_machining = True
        disc_sanding = True
        observation = nova_lista[1]
        code_semiacabado = nova_lista[0]
        is_active = True

        # print(refer, description, qnty, disc_preparation,
        #       disc_machining, disc_sanding, observation, refer_aux_father, is_active)

        django_add.append(
            Produtos(
                refer=refer,
                description=description,
                qtd_per_day=qtd_per_day,
                disc_prog=disc_prog,
                disc_preparation=disc_preparation,
                disc_machining=disc_machining,
                disc_sanding=disc_sanding,
                observation=observation,
                code_semiacabado=code_semiacabado,
                # is_active=is_active
            )
        )
    if len(django_add) > 0:
        Produtos.objects.bulk_create(django_add)
