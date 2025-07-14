# Flake8: noqa
import json
import os

NOME_ARQUIVO = 'teste.json'
CAMINHO_ABS_ARQUIVO = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        NOME_ARQUIVO
    )
)

filme = {
    'title': 'O Senhor dos Anéis: A Sociedade do Anel',
    'original_title': 'The Lord of the Rings: The Fellowship of the Ring',
    'is_movie': True,
    'imdb_rating': 8.8,
    'year': 2001,
    'characters': ['Frodo', "Sam", "Gandalf", "Legolas", 'Boromir'],
    'budget': None
}

#Exportar dados para o Json
with open(CAMINHO_ABS_ARQUIVO, 'w') as arquivo:
    json.dump(filme, arquivo)  #ensure_ascii=False,ident=2


#Abrir dados do Json
with open(CAMINHO_ABS_ARQUIVO, 'r') as arquivo:
    filme_do_json = json.load(arquivo)
    print(filme_do_json)
