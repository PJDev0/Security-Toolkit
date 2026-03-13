# analyzer.py
import argparse
import sys
from scapy.all import sniff, TCP, IP, Raw, UDP
from scapy.layers.http import HTTPRequest

class PacketSniffer:
    def __init__(self, interface=None, syn_threshold=10):
        self.interface = interface
        self.syn_threshold = syn_threshold
        self.syn_counter = 0
        self.last_src_ip = None

    def _parse_packet(self, packet):
        if not packet.haslayer(IP):
            return

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        if src_ip != self.last_src_ip:
            self.syn_counter = 0
            self.last_src_ip = src_ip

        if packet.haslayer(TCP):
            self._handle_tcp(packet, src_ip, dst_ip)
        elif packet.haslayer(UDP):
            print(f"[UDP] {src_ip} --> {dst_ip}")

    def _handle_tcp(self, packet, src_ip, dst_ip):
        sport = packet[TCP].sport
        dport = packet[TCP].dport
        flags = packet[TCP].flags

        if flags == 'S':
            self.syn_counter += 1
            if self.syn_counter >= self.syn_threshold:
                print(f"[!] ALERT: Potential SYN Scan detected from {src_ip}")
        else:
            self.syn_counter = 0

        print(f"[TCP] {src_ip}:{sport} --> {dst_ip}:{dport} | Flags: {flags}")

        if packet.haslayer(HTTPRequest):
            host = packet[HTTPRequest].Host.decode('utf-8', errors='ignore')
            path = packet[HTTPRequest].Path.decode('utf-8', errors='ignore')
            method = packet[HTTPRequest].Method.decode('utf-8', errors='ignore')
            print(f"\t[HTTP Request] {method} {host}{path}")

        if packet.haslayer(Raw):
            payload = packet[Raw].load
            print(f"\t[Payload] {payload[:40]}...")

    def start(self):
        try:
            print(f"[*] Sniffing on interface: {self.interface if self.interface else 'Default'}")
            print("[*] Press Ctrl+C to stop.\n")
            
            sniff(
                iface=self.interface, 
                prn=self._parse_packet, 
                store=False
            )
        except KeyboardInterrupt:
            print("\n[*] Capture stopped by user.")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Packet Analyzer for Network Forensics")
    parser.add_argument("-i", "--interface", type=str, help="Network interface to bind to")
    args = parser.parse_args()

    sniffer = PacketSniffer(interface=args.interface)
    sniffer.start()