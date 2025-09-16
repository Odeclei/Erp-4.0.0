def quebrar_texto_por_palavras(texto, tamanho_maximo):
    partes = []
    texto_restante = texto.strip()

    while len(texto_restante) > tamanho_maximo:
        indice_espaco = texto_restante.rfind(" ", 0, tamanho_maximo)

        if indice_espaco != -1:
            partes.append(texto_restante[:indice_espaco])
            texto_restante = texto_restante[indice_espaco + 1 :].strip()
        else:
            partes.append(texto_restante[:tamanho_maximo])
            texto_restante = texto_restante[tamanho_maximo:].strip()

    partes.append(texto_restante)

    return partes


def gerar_zpl_etiqueta(
    item_name,
    acabamento,
    index,
    pedido_number,
    item_cod,
    volume_at,
    volume_total,
    observation,
):
    item_name_lines = quebrar_texto_por_palavras(item_name, 30)[:3]
    observation_lines = quebrar_texto_por_palavras(observation, 30)[:3]

    item_name1 = item_name_lines[0]
    item_name2 = item_name_lines[1] if len(item_name_lines) > 1 else ""
    item_name3 = item_name_lines[2] if len(item_name_lines) > 2 else ""

    observation1 = observation_lines[0]
    observation2 = observation_lines[1] if len(observation_lines) > 1 else ""
    observation3 = observation_lines[2] if len(observation_lines) > 2 else ""

    texto = f"""
    ^XA
    ^FO45,30^A0N,45,45
    ^FD{item_name1}^FS
    
    ^FO45,80^A0N,45,45
    ^FD{item_name2}^FS
    
    ^FO45,130^A0N,45,45
    ^FD{item_name3}^FS


    ^FO45,190^A0N,30,30
    ^FDCODE: {item_cod}^FS

    ^FO45,230^A0N,30,30
    ^FDACAB: {acabamento}^FS

    ^FO45,290^A0N,30,30
    ^FDPEDIDO: {pedido_number}^FS

    ^FO280,290^A0N,30,30
    ^FDVOLUME: {volume_at} / {volume_total}^FS

    ^FO45,350^A0N,30,30
    ^FDOBS: {observation1}^FS
    ^FO45,390^A0N,30,30
    ^FD{observation2}^FS
    ^FO45,430^A0N,30,30
    ^FD{observation3}^FS

    ^FO550,220^BY3,3
    ^BQN,2,9,M,7
    ^FDLA,{index}-{item_cod}-{acabamento}^FS
    ^XZ
        """
    return texto
