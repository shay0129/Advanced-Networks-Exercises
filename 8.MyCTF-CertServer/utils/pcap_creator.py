from scapy.all import IP, TCP, wrpcap
from scapy.layers.tls.record import TLS, TLSChangeCipherSpec, TLSApplicationData
from scapy.layers.tls.handshake import (
    TLSClientHello, TLSServerHello, TLSCertificate, 
    TLSClientKeyExchange, TLSServerHelloDone
)
from protocols_packets import create_tls_packet, create_tcp_packet, get_request, ok_response

# Define IP addresses for server and clients
server_ip = "192.168.1.0"
client1_ip = "192.168.1.1"
client2_ip = "192.168.1.2"

# Initialize global sequence number
seq_num = 1000

def create_ssl_handshake(client_ip: str, server_ip: str, use_cert: bool = False) -> list:
    # Create a TLS handshake with the specified parameters

    # Client Hello
    client_hello = TLSClientHello()
    print(f"Client Hello: {client_hello.summary()}")

    # Server Hello, Certificate, Server Key Exchange, Server Hello Done
    if use_cert:
        server_hello = TLSServerHello()
        print(f"Server Hello: {server_hello.summary()}")
        multiple_messages = server_hello / TLSCertificate() / TLSClientKeyExchange() / TLSServerHelloDone()
    else:
        server_hello = TLSServerHello()
        print(f"Server Hello: {server_hello.summary()}")
        multiple_messages = server_hello / TLSClientKeyExchange() / TLSServerHelloDone()

    # Client Key Exchange and Change Cipher Spec
    multiple_client = TLSClientKeyExchange() / TLSChangeCipherSpec()

    # Construct the packets for the TLS handshake
    packets = [
        create_tls_packet(src_ip=client_ip, dst_ip=server_ip, sport=443, dport=443, tls_message=client_hello),
        create_tls_packet(src_ip=server_ip, dst_ip=client_ip, sport=443, dport=443, tls_message=multiple_messages),
        create_tls_packet(src_ip=client_ip, dst_ip=server_ip, sport=443, dport=443, tls_message=multiple_client),
    ]

    return packets

def create_application_data_packet(src_ip: str, dst_ip: str, sport: int, dport: int, data: bytes, seq: int = 0, ack: int = 0) -> TLS:
    # Construct the TLS Application Data packet
    tcp_packet = create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack)
    tls_data_packet = tcp_packet / TLS(msg=[TLSApplicationData(data)])
    print(f"Created Application Data Packet: {tls_data_packet.summary()}")
    return tls_data_packet

def main():
    global seq_num

    client1_tls_packets = create_ssl_handshake(client1_ip, server_ip, use_cert=True)
    client2_tls_packets = create_ssl_handshake(client2_ip, server_ip, use_cert=False)

    # Application data from client1 (GET request)
    client1_get_request = create_application_data_packet(
        client1_ip, server_ip, 443, 443, get_request, seq=seq_num
    )
    seq_num += len(client1_get_request[TCP].payload)  # Update seq_num for the next packet

    # Application data from server to client1 (200 OK response)
    server_ok_response = create_application_data_packet(
        server_ip, client1_ip, 443, 443, ok_response, seq=seq_num
    )
    seq_num += len(server_ok_response[TCP].payload)  # Update seq_num after server's response

    # Check if packets are created
    if not client1_tls_packets or not client2_tls_packets or not client1_get_request or not server_ok_response:
        print("No packets were created.")
    else:
        try:
            wrpcap("tls_traffic.pcap", client1_tls_packets)
            wrpcap("tls_traffic.pcap", client2_tls_packets, append=True)
            wrpcap("tls_traffic.pcap", client1_get_request, append=True)
            wrpcap("tls_traffic.pcap", server_ok_response, append=True)
        except Exception as e:
            print(f"Error writing packets to pcap file: {e}")

if __name__ == "__main__":
    main()
