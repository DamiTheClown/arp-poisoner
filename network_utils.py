from scapy.all import Ether, ARP, srp
import platform
import atexit
import os

# --- Config --- #
ip_addr = input("[?] Zadejte IP adresu včetně prefixu (např. 192.168.1.1/24): ")
ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast
arp = ARP(pdst=ip_addr)

# --- Sken sítě --- #
def scan_network():
    counter = 0
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    for sent, received in result:
        counter += 1
        print(f"{counter}. | IP: {received.psrc} | MAC: {received.hwsrc}")

# --- IP forwarding --- #
def toggle_forwarding(enable=True):
    system = platform.system()

    if system == "Linux":
        value = "1" if enable else "0"
        os.system(f"sysctl -w net.ipv4.ip_forward={value}")

    elif system == "Windows":
        value = "enabled" if enable else "disabled"
        os.system(f"netsh interface ipv4 set global forwarding={value}")

    else:
        print("[-] Neznámý operační systém. Nelze nastavit IP forwarding.")

# --- Cleanup při ukončení --- #
def cleanup():
    print("\n[+] Vypínám IP forwarding...")
    toggle_forwarding(False)

atexit.register(cleanup)

# --- Main --- #
if __name__ == "__main__":
    scan_network()
    print("\n[+] Zapínám IP forwarding...")
    toggle_forwarding(True)
