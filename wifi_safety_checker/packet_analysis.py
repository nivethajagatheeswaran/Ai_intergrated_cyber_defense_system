from scapy.all import sniff, IP
from collections import defaultdict

def analyze_packets(packet_count=20):
    ip_counter = defaultdict(int)

    def process_packet(packet):
        if IP in packet:
            src_ip = packet[IP].src
            ip_counter[src_ip] += 1

    sniff(count=packet_count, prn=process_packet)

    suspicious_ips = []

    for ip, count in ip_counter.items():
        if count > 10:
            suspicious_ips.append({
                "ip": ip,
                "packet_count": count
            })

    return suspicious_ips