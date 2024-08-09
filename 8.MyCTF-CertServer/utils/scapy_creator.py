from scapy.all import IP, TCP, wrpcap
from scapy.layers.tls.record import TLS
from scapy.layers.tls.handshake import (
    TLSClientHello, TLSServerHello, TLSCertificate, 
    TLSClientKeyExchange, TLSFinished, TLSServerHelloDone
)

# Initialize global sequence number
seq_num = 1000

# Define IP addresses for server and clients
server_ip = "192.168.1.1"
client1_ip = "192.168.1.2"
CN = "Pasdaran.local"

def create_tcp_packet(src_ip: str, dst_ip: str, sport: int, dport: int, flags: str, seq: int = 0, ack: int = 0) -> TCP:
    global seq_num
    packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags=flags, seq=seq_num if seq == 0 else seq, ack=ack)
    seq_num += len(packet[TCP].payload) if packet.haslayer(TCP) else 0
    print(f"Created TCP Packet: {packet.summary()}")
    return packet

def create_tls_packet(src_ip: str, dst_ip: str, sport: int, dport: int, tls_message, seq: int = 0, ack: int = 0) -> TLS:
    tcp_packet = create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack)
    tls_packet = tcp_packet / TLS(msg=[tls_message])
    print(f"Created TLS Packet: {tls_packet.summary()}")
    return tls_packet

def create_ssl_handshake(client_ip: str, use_cert: bool = False) -> list:
    global seq_num

    # Client Hello
    client_hello = TLSClientHello()
    cipher_suites = [0xc02b, 0xc02f, 0xc030, 0xc00a]  # Example cipher suites
    client_hello.cipher_suites = cipher_suites
    print(f"Client Hello: {client_hello.summary()}")

    # Server Hello
    server_hello = TLSServerHello()
    print(f"Server Hello: {server_hello.summary()}")

    cert_layer = TLSCertificate()
        
    server_hello_done = TLSServerHelloDone()
    client_key_exchange = TLSClientKeyExchange()
    client_finished = TLSFinished()
    server_finished = TLSFinished()

    # Construct the packets for the TLS handshake
    packets = [
        create_tls_packet(client_ip, server_ip, 443, 443, client_hello),
        create_tls_packet(server_ip, client_ip, 443, 443, server_hello),
    ]

    if cert_layer:
        packets.append(create_tls_packet(server_ip, client_ip, 443, 443, cert_layer))
        
    packets += [
        create_tls_packet(server_ip, client_ip, 443, 443, server_hello_done),
        create_tls_packet(client_ip, server_ip, 443, 443, client_key_exchange),
        create_tls_packet(server_ip, client_ip, 443, 443, client_finished),
        create_tls_packet(server_ip, client_ip, 443, 443, server_finished)
    ]

    return packets

# Main Logic
packets = create_ssl_handshake(client1_ip, use_cert=True)

# Check if packets are created
if not packets:
    print("No packets were created.")
else:
    try:
        wrpcap("tls_traffic.pcap", packets)
        print("PCAP file created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the PCAP file: {e}")
