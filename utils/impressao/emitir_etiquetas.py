import usb.core
import usb.util

# Nome da impressora
printer_name = "\\\\vendas01\\ZDesigner TLP 2844ZDesigner TLP 2844"

# ID do dispositivo da impressora
printer_id = (0x0A5F, 0x0001)  # ID do dispositivo da Zebra TLP 2844

# Conecte-se à impressora
dev = usb.core.find(idVendor=printer_id[0], idProduct=printer_id[1])

# Verifique se a impressora está conectada
if dev is None:
    print("Impressora não encontrada")
else:
    print("Impressora conectada")
