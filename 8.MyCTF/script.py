from scapy.all import Ether, IP, TCP, Raw, PcapWriter
from scapy.layers.tls.handshake import TLSClientHello, TLSServerHello
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

def create_self_signed_cert():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost")
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())

    return cert, key

def create_pcapng(filename):
    with PcapWriter(filename, append=False, sync=True) as writer:
        # Example packets
        client_ip = '192.168.1.2'
        server_ip = '192.168.1.1'
        port = 443
        mac_client = '00:11:22:33:44:55'
        mac_server = '55:44:33:22:11:00'
        
        # Client Hello
        client_hello = TLSClientHello()
        client_pkt = (
            Ether(src=mac_client, dst=mac_server)
            / IP(src=client_ip, dst=server_ip)
            / TCP(sport=12345, dport=port)
            / client_hello
        )
        writer.write(client_pkt)

        # Server Hello
        server_hello = TLSServerHello()
        server_pkt = (
            Ether(src=mac_server, dst=mac_client)
            / IP(src=server_ip, dst=client_ip)
            / TCP(sport=port, dport=12345)
            / server_hello
        )
        writer.write(server_pkt)

if __name__ == "__main__":
    create_pcapng("example.pcapng")
