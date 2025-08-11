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

    texto = f"""
^XA
^FO45,30^A0N,40,40
^FD{item_name}^FS

^FO45,90^A0N,30,30
^FDCODE: {item_cod}^FS

^FO45,130^A0N,30,30
^FDACAB: {acabamento}^FS

^FO45,300^A0N,30,30
^FDPEDIDO: {pedido_number}^FS

^FO250,300^A0N,30,30
^FDVOLUME: {volume_at}/{volume_total}^FS

^FO45,350^A0N,30,30
^FDOBS: {observation}^FS

^FO520,220^BY3,3
^BQN,2,9,M,7
^FDLA,{index}-{item_cod}-{acabamento}^FS
^XZ
    """
    return texto


# def imprimir_zpl(zpl):
#     with open(r"\\vendas01\ZDesigner TLP 2844", "w") as printer:
#         printer.write(zpl)


# def imprimir_zpl(zpl, printer_name="ZDesigner TLP 2844"):
#     hPrinter = win32print.OpenPrinter(printer_name)
#     hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta Pedido", None, "RAW"))
#     win32print.StartPagePrinter(hPrinter)
#     win32print.WritePrinter(hPrinter, zpl.encode())
#     win32print.EndPagePrinter(hPrinter)
#     win32print.EndDocPrinter(hPrinter)
#     win32print.ClosePrinter(hPrinter)
