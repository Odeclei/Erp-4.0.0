# print_server.py
import win32print
from flask import Flask, request, jsonify
import threading
import pystray
from PIL import Image


# --- Configuração ---
# O nome da impressora como aparece no Windows.
# Se a impressora estiver compartilhada, pode ser o caminho de rede.
# Se estiver conectada localmente via USB, é apenas o nome dela.
printer_path = r"\\vendas01\ZDesigner TLP 2844"
# PRINTER_NAME = "ZDesigner TLP 2844" || printer_path
PRINTER_NAME = printer_path
# O IP do computador vendas01. Use '0.0.0.0' para aceitar conexões de qualquer IP na rede.
HOST_IP = "0.0.0.0"
PORT = 5001  # Porta que o serviço vai escutar.

app = Flask(__name__)
# Variável para controlar o estado do servidor
server_thread = None


def imprimir_zpl(zpl_code):
    """
    Envia o código ZPL para a impressora especificada.
    """
    try:
        hPrinter = win32print.OpenPrinter(PRINTER_NAME)
        try:
            hJob = win32print.StartDocPrinter(
                hPrinter, 1, ("Etiqueta ZPL", None, "RAW")
            )
            try:
                win32print.StartPagePrinter(hPrinter)
                # O ZPL precisa ser enviado como bytes
                win32print.WritePrinter(hPrinter, zpl_code.encode("utf-8"))
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
        return True, "Etiqueta enviada para a impressora com sucesso."
    except Exception as e:
        # Log do erro para diagnóstico
        print(f"Erro ao imprimir: {e}")
        return False, f"Erro ao comunicar com a impressora: {e}"


@app.route("/print", methods=["POST"])
def print_label():
    """
    Endpoint que recebe o ZPL e manda para a função de impressão.
    """
    if not request.json or "zpl" not in request.json:
        return (
            jsonify(
                {"success": False, "message": "Payload inválido. 'zpl' não encontrado."}
            ),
            400,
        )

    zpl = request.json["zpl"]
    success, message = imprimir_zpl(zpl)

    if success:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "message": message}), 500


def run_flask_server():
    """
    Função que inicia o servidor Flask.
    """
    global server_thread
    if server_thread and server_thread.is_alive():
        print("Servidor já está rodando.")
        return

    # Usamos `app.run` com `threaded=True` para não bloquear a thread principal,
    # embora a thread que estamos criando já resolva isso.
    # O `use_reloader=False` é importante para não criar múltiplas instâncias
    # do servidor ao rodar como executável.
    server_thread = threading.Thread(
        target=app.run,
        kwargs={"host": HOST_IP, "port": PORT, "debug": False, "use_reloader": False},
    )
    server_thread.daemon = (
        True  # Permite que a thread seja encerrada junto com o programa principal
    )
    server_thread.start()
    print(f"Servidor de impressão rodando em http://{HOST_IP}:{PORT}")
    print(f"Escutando por pedidos de impressão para a impressora: '{PRINTER_NAME}'")


def on_quit(icon, item):
    """
    Função chamada quando o usuário clica em 'Sair'.
    """
    print("Encerrando o servidor e saindo...")
    icon.stop()  # Interrompe o ícone na bandeja
    # A thread do Flask será encerrada automaticamente pois é uma daemon thread


try:
    image = Image.open("print_icon.png")
except FileNotFoundError:
    print("Aviso: 'icon.png' não encontrado. Usando ícone padrão.")
    image = Image.new("RGB", (64, 64), color="red")

# Criando o ícone na bandeja com seu menu
icon = pystray.Icon(
    "print_server",
    image,
    "Servidor de Impressão",
    menu=pystray.Menu(
        pystray.MenuItem("Iniciar Servidor", run_flask_server),
        pystray.MenuItem("Sair", on_quit),
    ),
)

if __name__ == "__main__":
    # Inicia o servidor ao abrir o programa
    run_flask_server()
    # Roda o ícone na bandeja do sistema. Isso mantém o programa rodando.
    icon.run()
# if __name__ == '__main__':
#     print(f"Servidor de impressão rodando em http://{HOST_IP}:{PORT}")
#     print(f"Escutando por pedidos de impressão para a impressora: '{PRINTER_NAME}'")
#     app.run(host=HOST_IP, port=PORT, debug=False)
