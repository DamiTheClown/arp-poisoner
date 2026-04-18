# spoofer_logic.py - TODO LIST

# 1. TODO: Importovat Scapy (ARP, send, wrpcap)

# 2. TODO: Funkce spoof(target_ip, spoof_ip, target_mac)
#    - Vytvořit falešný ARP paket typu "is-at".
#    - Nastavit psrc na IP routeru, ale odeslat ho na MAC oběti.

# 3. TODO: Funkce restore(target_ip, gateway_ip, target_mac, gateway_mac)
#    - Pošle správné ARP údaje oběti i routeru.
#    - Tím se síť "uzdraví", až vypnete program.

# 4. TODO: Funkce save_capture(packet_list, filename="capture.pcap")
#    - Použít wrpcap() k uložení nasbíraných dat.
from scapy.all import ARP, send, wrpcap, sr1, sr

def spoof():

    ip_obet = input("Zadejte IP adresu oběti: ")
    ip_router = input("Zadejte IP adresu routeru: ")

    mac_obet = sr1(ARP(pdst=ip_obet), timeout=2, verbose=False).hwsrc
    mac_router = sr1(ARP(pdst=ip_router), timeout=2, verbose=False).hwsrc

    if mac_obet is None:
        print(f"Nepodařilo se získat MAC adresu oběti ({ip_obet}).")
    
    if mac_router is None:
        print(f"Nepodařilo se získat MAC adresu routeru ({ip_router}).")

    
