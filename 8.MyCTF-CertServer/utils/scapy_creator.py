from scapy.all import IP, TCP, wrpcap
from scapy.layers.tls.record import TLS, TLSChangeCipherSpec
from scapy.layers.tls.handshake import (
    TLSClientHello, TLSServerHello, TLSCertificate, 
    TLSClientKeyExchange, TLSFinished, TLSServerHelloDone, 
)
# Initialize global sequence number
seq_num = 1000

# Define IP addresses for server and clients
server_ip = "192.168.1.0"
client1_ip = "192.168.1.1"
client2_ip = "192.168.1.2"
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
    print(f"Client Hello: {client_hello.summary()}")

    # Multiple Handshake Messages:
    multiple_messages = None
    if use_cert:
        # Server Hello, Certificate, Server Key Exchange, Server Hello Done
        server_hello = TLSServerHello()
        print(f"server Hello: {server_hello.summary()}")
        multiple_messages = server_hello / TLSCertificate() / TLSClientKeyExchange() / TLSServerHelloDone()
    else:
        # Server Hello, Server Key Exchange, Server Hello Done
        server_hello = TLSServerHello()
        cipher_suite = 0xc02b  # chosen by server
        server_hello.cipher_suite = cipher_suite
        print(f"server Hello: {server_hello.summary()}")
        multiple_messages = server_hello / TLSClientKeyExchange() / TLSServerHelloDone()


    # Server Hello
    server_hello = TLSServerHello()
    cipher_suite = 0xc02b  # chosen by server
    server_hello.cipher_suite = cipher_suite
    print(f"server Hello: {server_hello.summary()}")
    # Certificate, Client Key Exchange, Finished, Server Hello Done

    multiple_messages = server_hello / TLSCertificate() / TLSClientKeyExchange() / TLSFinished() / TLSServerHelloDone()


    multiple_client = TLSClientKeyExchange() / TLSChangeCipherSpec()
    # Construct the packets for the TLS handshake
    packets = [
        create_tls_packet(client_ip, server_ip, 443, 443, client_hello),
        create_tls_packet(server_ip, client_ip, 443, 443, multiple_messages),
        create_tls_packet(server_ip, client_ip, 443, 443, multiple_client),

    ]
    return packets

def create_http_packet(src_ip: str, dst_ip: str, sport: int, dport: int, flags: str, seq: int = 0, ack: int = 0) -> TCP:
    http_data = b"GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
    packet = create_tcp_packet(src_ip, dst_ip, sport, dport, flags, seq, ack) / http_data
    print(f"Created HTTP Packet: {packet.summary()}")
    return packet

def main():
    client1_tls_packets = create_ssl_handshake(client1_ip, True)
    cleint1_http_packets = create_http_packet(client1_ip, server_ip, 443, 443, "PA", seq_num, 0)
    client2_tls_packets = create_ssl_handshake(client2_ip, False)
    cleint2_http_packets = create_http_packet(client2_ip, server_ip, 443, 443, "PA", seq_num, 0)

    # Check if packets are created
    if not client1_tls_packets or not client2_tls_packets or cleint1_http_packets or cleint2_http_packets:
        print("No packets were created.")
    else:
        try:
            wrpcap("tls_traffic.pcap", client1_tls_packets)
            wrpcap("tls_traffic.pcap", client1_tls_packets, append=True)
            wrpcap("tls_traffic.pcap", cleint1_http_packets, append=True)
            wrpcap("tls_traffic.pcap", client2_tls_packets, append=True)

            print("PCAP file created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the PCAP file: {e}")

if __name__ == "__main__":
    main()
