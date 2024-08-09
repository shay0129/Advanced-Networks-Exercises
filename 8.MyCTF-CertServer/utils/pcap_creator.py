from scapy.all import wrpcap
from scapy.layers.tls.record import TLS, TLSChangeCipherSpec, TLSApplicationData
from scapy.layers.tls.handshake import (
    TLSClientHello, TLSServerHello, TLSCertificate, 
    TLSClientKeyExchange, TLSServerHelloDone, TLSFinished
)
from protocols_packets import create_tls_packet, create_tcp_packet, get_request, ok_response

# Define IP addresses for server and clients
server_ip = "192.168.1.0"
client1_ip = "192.168.1.1"
client2_ip = "192.168.1.2"

# Initialize global sequence numbers
seq_num_client1 = 1000
seq_num_server = 2000
seq_num_client2 = 3000

ack_num_client1 = 0
ack_num_client2 = 0

def create_ssl_handshake(client_ip: str, server_ip: str, seq_num: int, ack_num: int, use_cert: bool = False) -> list:
    packets = []

    # Client Hello
    client_hello = TLSClientHello()
    packet = create_tls_packet(
        client_ip,
        server_ip,
        sport=443,
        dport=443,
        tls_message=client_hello,
        seq=seq_num,
        ack=ack_num
    )
    seq_num += len(client_hello)
    ack_num += len(client_hello) 
    packets.append(packet)

    # Server Hello, Certificate (optional), Server Hello Done
    server_hello = TLSServerHello()
    server_records = server_hello 
    if use_cert:
        server_records /= TLSCertificate() 
        
    server_records /= TLSServerHelloDone()
    packet = create_tls_packet(
        server_ip,
        client_ip,
        sport=443,
        dport=443,
        tls_message=server_records,
        seq=seq_num,
        ack=ack_num
    )
    seq_num += len(server_records)
    ack_num += len(server_records) 
    packets.append(packet)

    # Client Key Exchange, Change Cipher Spec, Finished
    client_key_exchange = TLSClientKeyExchange()
    change_cipher_spec_client = TLSChangeCipherSpec()
    finished_client = TLSFinished()
    client_records = client_key_exchange / change_cipher_spec_client / finished_client

    packet = create_tls_packet(
        client_ip,
        server_ip,
        sport=443,
        dport=443,
        tls_message=client_records,  # List of messages
        seq=seq_num,
        ack=ack_num
    )
    seq_num += len(client_records)
    ack_num += len(client_records) 
    packets.append(packet)

    # Server Change Cipher Spec, Finished
    change_cipher_spec_server = TLSChangeCipherSpec()
    finished_server = TLSFinished()
    server_records = change_cipher_spec_server / finished_server
    packet = create_tls_packet(
        server_ip,
        client_ip,
        sport=443,
        dport=443,
        tls_message=server_records,
        seq=seq_num,
        ack=ack_num
    )
    seq_num += len(server_records)
    ack_num += len(server_records) 
    packets.append(packet)

    return packets, seq_num, ack_num

def create_application_data_packet(src_ip: str, dst_ip: str, sport: int, dport: int, data: bytes, seq: int = 0, ack: int = 0) -> TLS:
    # Construct the TLS Application Data packet
    tls_data_packet = create_tcp_packet(src_ip, dst_ip, sport, dport, "PA", seq, ack) / TLS(msg=[TLSApplicationData(data)])
    seq += len(data)
    return tls_data_packet, seq

def main():
    global seq_num_client1, seq_num_server, seq_num_client2, ack_num_client1, ack_num_client2

    # TLS handshake packets for client1 and server
    client1_tls_packets, seq_num_client1, ack_num_client1 = create_ssl_handshake(client1_ip, server_ip, seq_num_client1, ack_num_client1, use_cert=True)
    
    # Application data from client1 (GET request)
    client1_get_request, seq_num_client1 = create_application_data_packet(client1_ip, server_ip, 443, 443, get_request, seq=seq_num_client1, ack=ack_num_client1)
    ack_num_server = seq_num_client1

    # Application data from server to client1 (200 OK response)
    server_ok_response, seq_num_server = create_application_data_packet(server_ip, client1_ip, 443, 443, ok_response, seq=seq_num_server, ack=ack_num_server)

    # TLS handshake packets for client2 and server
    client2_tls_packets, seq_num_client2, ack_num_client2 = create_ssl_handshake(client2_ip, server_ip, seq_num_client2, ack_num_client2, use_cert=False)

    # Check if packets are created
    if not client1_tls_packets or not client1_get_request or not server_ok_response or not client2_tls_packets:
        print("No packets were created.")
    else:
        try:
            wrpcap("tls_traffic.pcap", client1_tls_packets + [client1_get_request, server_ok_response] + client2_tls_packets)
            print("Packets successfully written to pcap file.")
        except Exception as e:
            print(f"Error writing packets to pcap file: {e}")

if __name__ == "__main__":
    main()