from scapy.all import IP, TCP, wrpcap
from scapy.layers.tls.handshake import TLSClientHello, TLSServerHello, TLSClientKeyExchange, TLSFinished, TLSServerHelloDone
from scapy.layers.tls.record import TLS
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.http import Raw
import os
import sslkeylog # Import the sslkeylog library

sslkeylog.set_keylog(os.environ.get('SSLKEYLOGFILE')) # catche the pre-master secret in the SSLKEYLOGFILE environment variable

# Initialize global sequence number
seq_num = 1000  # You can start from any arbitrary number

# Define IP addresses for server and clients
server_ip = "192.168.1.1"
client1_ip = "192.168.1.2"  # Client with cert
client2_ip = "192.168.1.3"  # Client without cert
CN = "Pasdaran.local"

def create_tcp_packet(src_ip, dst_ip, sport, dport, flags, seq=0, ack=0):
    global seq_num
    packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags=flags, seq=seq_num, ack=ack)
    seq_num += len(packet[TCP].payload)
    return packet

def create_tls_packet(src_ip, dst_ip, sport, dport, tls_message, seq=0, ack=0):
    return create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack) / TLS(msg=[tls_message])

def create_http_packet(src_ip, dst_ip, sport, dport, http_message, body=b"", seq=0, ack=0):
    return create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack) / http_message / Raw(load=body)

def create_ssl_handshake(client_ip, use_cert=False):
    global seq_num

    # Client Hello
    client_hello = TLSClientHello()
    cipher_suites = [0xc02b, 0xc02f, 0xc030, 0xc00a]  # Example cipher suites
    client_hello.cipher_suites = cipher_suites

    # Server Hello
    server_hello = TLSServerHello()
    if use_cert:
        try:
            with open(f"{CN}.crt", "rb") as f:
                cert_data = f.read()
            server_hello.certificates = cert_data  # Assuming the certificate is in DER format
        except FileNotFoundError as e:
            print(f"Error loading certificate: {e}")
            return []

    server_hello_done = TLSServerHelloDone()

    client_key_exchange = TLSClientKeyExchange()
    client_finished = TLSFinished()
    server_finished = TLSFinished()

    # Construct the packets for the TLS handshake
    packets = [
        create_tls_packet(client_ip, server_ip, 443, 443, client_hello),
        create_tls_packet(server_ip, client_ip, 443, 443, server_hello),
        create_tls_packet(server_ip, client_ip, 443, 443, server_hello_done),
        create_tls_packet(client_ip, server_ip, 443, 443, client_key_exchange),
        create_tls_packet(client_ip, server_ip, 443, 443, client_finished),
        create_tls_packet(server_ip, client_ip, 443, 443, server_finished)
    ]
    return packets

# Main Logic
packets = []

# Handshake with certificate
packets += create_ssl_handshake(client1_ip, use_cert=True) 
packets += [
    create_http_packet(client1_ip, server_ip, 443, 443, HTTPRequest(Method="GET", Path="/resource"), body=b""),
    create_http_packet(server_ip, client1_ip, 443, 443, HTTPResponse(Status_Code=200, Reason_Phrase="OK"), body=b"Resource Data")
]

# Handshake without certificate
packets += create_ssl_handshake(client2_ip, use_cert=False)  
packets += [
    create_http_packet(client2_ip, server_ip, 443, 443, HTTPRequest(Method="GET", Path="/resource"), body=b""),
    create_http_packet(server_ip, client2_ip, 443, 443, HTTPResponse(Status_Code=400, Reason_Phrase="Bad Request"), body=b"Missing Certificate")
]

try:
    wrpcap("tls_traffic.pcap", packets)
    print("PCAP file created successfully.")
except Exception as e:
    print(f"An error occurred while creating the PCAP file: {e}")