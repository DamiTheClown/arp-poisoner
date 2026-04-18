
# 4. TODO: Funkce toggle_forwarding(enable=True)
#    - Pokud enable=True, zapsat "1" do /proc/sys/net/ipv4/ip_forward
#    - Pokud enable=False, zapsat "0" (uklidit po sobě).
#    - Tip: Použij os.system() nebo os.popen().

from scapy.all import *
import os


# --- Config --- # 
ip_addr = input("Zadejte IP adresu včetně prefixu (např. 192.168.1.1/24): ")
ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast
arp = ARP(pdst=ip_addr)
id = 0

# --- Sken sítě --- #
def scan_network():
    global id  # ID jako globální proměnná
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    for sent, received in result:
        id += 1
        print(f"{id}. IP: {received.psrc}, MAC: {received.hwsrc}")

scan_network()