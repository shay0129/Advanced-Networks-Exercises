from scapy.all import IP, TCP
from scapy.layers.tls.record import TLS

get_request = b"GET /resource HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
ok_response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nHello, world!"
seq_num = 1000

# Layer 3
def create_ip_packet(src_ip: str, dst_ip: str) -> IP:
    # Create an IP packet with the specified source and destination IP addresses
    packet = IP(src=src_ip, dst=dst_ip)
    print(f"Created IP Packet: {packet.summary()}")
    return packet

# Layer 4
def create_tcp_packet(src_ip: str, dst_ip: str, sport: int, dport: int, flags: str, seq: int = 0, ack: int = 0) -> TCP:
    # Create a TCP packet with the specified parameters
    global seq_num
    packet = create_ip_packet(src_ip, dst_ip) / TCP(sport=sport, dport=dport, flags=flags, seq=seq_num if seq == 0 else seq, ack=ack)
    seq_num += len(packet[TCP].payload) if packet.haslayer(TCP) else 0
    print(f"Created TCP Packet: {packet.summary()}")
    return packet

# Layer 4
def create_tls_packet(src_ip: str, dst_ip: str, sport: int, dport: int, tls_message, seq: int = 0, ack: int = 0) -> TLS:
    # Create a TLS packet with the specified parameters
    tcp_packet = create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack)

    # Ensure tls_message is always a list, even if it's a single message
    if not isinstance(tls_message, list):
        tls_message = [tls_message]

    tls_packet = tcp_packet / TLS(msg=tls_message)
    print(f"Created TLS Packet: {tls_packet.summary()}")
    return tls_packet


# Layer 5
def create_http_packet(src_ip: str, dst_ip: str, sport: int, dport: int, flags: str, seq: int = 0, ack: int = 0) -> TCP:
    # Create an HTTP packet with the specified parameters
    http_data = b"GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
    packet = create_tcp_packet(src_ip, dst_ip, sport, dport, flags, seq, ack) / http_data
    print(f"Created HTTP Packet: {packet.summary()}")
    return packet