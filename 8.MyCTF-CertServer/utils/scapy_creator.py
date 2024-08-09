from scapy.all import IP, TCP, wrpcap
from scapy.layers.tls.record import TLS, TLSChangeCipherSpec
from scapy.layers.tls.handshake import (
    TLSClientHello, TLSServerHello, TLSCertificate, 
    TLSClientKeyExchange, TLSServerHelloDone
)

# Initialize global sequence number
seq_num = 1000

# Define IP addresses for server and clients
server_ip = "192.168.1.0"
client1_ip = "192.168.1.1"
client2_ip = "192.168.1.2"
CN = "Pasdaran.local"

def create_tcp_packet(src_ip: str, dst_ip: str, sport: int, dport: int, flags: str, seq: int = 0, ack: int = 0) -> TCP:
    # Create a TCP packet with the specified parameters
    global seq_num
    packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags=flags, seq=seq_num if seq == 0 else seq, ack=ack)
    seq_num += len(packet[TCP].payload) if packet.haslayer(TCP) else 0
    print(f"Created TCP Packet: {packet.summary()}")
    return packet

def create_tls_packet(src_ip: str, dst_ip: str, sport: int, dport: int, tls_message, seq: int = 0, ack: int = 0) -> TLS:
    # Create a TLS packet with the specified parameters
    tcp_packet = create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack)
    tls_packet = tcp_packet / TLS(msg=[tls_message])
    print(f"Created TLS Packet: {tls_packet.summary()}")
    return tls_packet

def create_ssl_handshake(client_ip: str, server_ip: str, use_cert: bool = False) -> list:
    # Create a TLS handshake with the specified parameters
    global seq_num

    # Client Hello
    client_hello = TLSClientHello()
    print(f"Client Hello: {client_hello.summary()}")

    # Multiple Handshake Messages
    if use_cert:
        # Server Hello, Certificate, Server Key Exchange, Server Hello Done
        server_hello = TLSServerHello()
        print(f"Server Hello: {server_hello.summary()}")
        multiple_messages = server_hello / TLSCertificate() / TLSClientKeyExchange() / TLSServerHelloDone()
    else:
        # Server Hello, Server Key Exchange, Server Hello Done
        server_hello = TLSServerHello()
        print(f"Server Hello: {server_hello.summary()}")
        multiple_messages = server_hello / TLSClientKeyExchange() / TLSServerHelloDone()

    # Client Key Exchange and Change Cipher Spec
    multiple_client = TLSClientKeyExchange() / TLSChangeCipherSpec()

    # Construct the packets for the TLS handshake
    packets = [
        create_tls_packet(src_ip=client_ip, dst_ip=server_ip, sport=443, dport=443, tls_message=client_hello),
        create_tls_packet(src_ip=server_ip, dst_ip=client_ip, sport=443, dport=443, tls_message=multiple_messages),
        create_tls_packet(src_ip=server_ip, dst_ip=client_ip, sport=443, dport=443, tls_message=multiple_client)
    ]

    return packets

def create_http_packet(src_ip: str, dst_ip: str, sport: int, dport: int, flags: str, seq: int = 0, ack: int = 0) -> TCP:
    # Create an HTTP packet with the specified parameters
    http_data = b"GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
    packet = create_tcp_packet(src_ip, dst_ip, sport, dport, flags, seq, ack) / http_data
    print(f"Created HTTP Packet: {packet.summary()}")
    return packet

def main():
    client1_tls_packets = create_ssl_handshake(client1_ip, server_ip, use_cert=True)
    client1_http_packets = create_http_packet(client1_ip, server_ip, 81, 81, "PA", seq_num, 0)
    client2_tls_packets = create_ssl_handshake(client2_ip, server_ip, use_cert=False)
    client2_http_packets = create_http_packet(client2_ip, server_ip, 81, 81, "PA", seq_num, 0)

    # Check if packets are created
    if not client1_tls_packets or not client2_tls_packets or not client1_http_packets or not client2_http_packets:
        print("No packets were created.")
    else:
        try:
            wrpcap("tls_traffic.pcap", client1_tls_packets)
            wrpcap("tls_traffic.pcap", client1_http_packets, append=True)
            wrpcap("tls_traffic.pcap", client2_tls_packets, append=True)
            wrpcap("tls_traffic.pcap", client2_http_packets, append=True)
        except Exception as e:
            print(f"Error writing packets to pcap file: {e}")

if __name__ == "__main__":
    main()
