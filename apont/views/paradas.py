# flake8: noqa
import datetime
import json
from pickle import FALSE

from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apont.models import Stops, StopsCategory, StopsMotive
from rule.models import Machines


def StopsMotiveView(request):
    stops_group = StopsCategory.objects.all()
    data_atual = datetime.datetime.now()
    momento_parada = data_atual.strftime("%d/%m/%y %H:%M:%S")

    context = {
        'stops_group': stops_group,
        'momento_parada': momento_parada,
    }
    return render(
        request,
        'apont/stops_group.html',
        context
    )


@csrf_exempt
def SubgrupoStop(request):
    if request.method == 'POST':
        dados_form = request.POST
        id_category = dados_form['id_category']

        subgrupos = StopsMotive.objects.filter(
            category=id_category).order_by('category')
        subgrupo_serializer = serializers.serialize(
            'json', subgrupos)  # No need for json.loads

        sub_json = json.loads(subgrupo_serializer)
        # Create a list of dictionaries directly from the queryset
        sub_data = []
        for item in sub_json:
            sub_data.append({'id': item['pk'], 'fields': item['fields']})

        return JsonResponse(sub_data, safe=False)

    return JsonResponse({'att': 'OK'})


@csrf_exempt
def ApontStop(request, *args, **kwargs):
    if request.method == "POST":
        dados_form = request.POST
        machine_id = dados_form['id_machine']
        motive_id = dados_form['motive_id']
        data_parada = dados_form['hr_parada']

        data_parada_str = data_parada
        formato_data = "%d/%m/%y %H:%M:%S"
        data_inicial = datetime.datetime.strptime(
            data_parada_str, formato_data)

        data_atual = datetime.datetime.now()
        data = data_atual.strftime("%Y-%m-%d")
        diferenca = data_atual-data_inicial

        diferenca_segundos = int(diferenca.total_seconds()+30)

        machine = Machines.objects.get(pk=machine_id)
        motive = StopsMotive.objects.get(pk=motive_id)
        user = User.objects.get(pk=request.user.id)

        dados = {
            'machine': machine,
            'date': data,
            'motive': motive,
            'duration': diferenca_segundos,
            'user': user,
        }

        model = Stops
        novo_apontamento = model(**dados)
        novo_apontamento.save()

        print(diferenca_segundos)

        data = {
            'apont': 'ok',
            "timestop": diferenca_segundos,
        }

        return JsonResponse(data, safe=False)

    return JsonResponse({"apont": "not ok"})
