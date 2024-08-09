from scapy.all import Ether, IP, TCP, Raw, PcapWriter, RandMAC, RandShort

def create_pcapng(filename):
    with PcapWriter(filename, append=False, sync=True) as writer:
        # IPs and ports
        client1_ip = '192.168.1.2'
        client2_ip = '192.168.1.3'
        server_ip = '192.168.1.1'
        server_port = 443

        # MAC addresses
        client1_mac = RandMAC()
        client2_mac = RandMAC()
        server_mac = RandMAC()

        # Define source ports
        client1_sport = RandShort()
        client2_sport = RandShort()

        # Client 1 TCP SYN Packet
        client1_syn = (
            Ether(src=client1_mac, dst=server_mac) 
            / IP(src=client1_ip, dst=server_ip) 
            / TCP(sport=client1_sport, dport=server_port, flags='S')
        )
        writer.write(client1_syn)

        # Server TCP SYN-ACK Packet
        server_syn_ack = (
            Ether(src=server_mac, dst=client1_mac) 
            / IP(src=server_ip, dst=client1_ip) 
            / TCP(sport=server_port, dport=client1_sport, flags='SA')
        )
        writer.write(server_syn_ack)

        # Client 1 TCP ACK Packet
        client1_ack = (
            Ether(src=client1_mac, dst=server_mac) 
            / IP(src=client1_ip, dst=server_ip) 
            / TCP(sport=client1_sport, dport=server_port, flags='A')
        )
        writer.write(client1_ack)

        # Client 1 HTTP GET Request
        client1_get = (
            Ether(src=client1_mac, dst=server_mac) 
            / IP(src=client1_ip, dst=server_ip) 
            / TCP(sport=client1_sport, dport=server_port) 
            / Raw(load="GET /resource.png HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
        )
        writer.write(client1_get)

        # Server HTTP 400 Bad Request Response
        server_400_response = (
            Ether(src=server_mac, dst=client1_mac) 
            / IP(src=server_ip, dst=client1_ip) 
            / TCP(sport=server_port, dport=client1_sport) 
            / Raw(load="HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nNo certificate provided".encode())
        )
        writer.write(server_400_response)

        # Client 2 TCP SYN Packet
        client2_syn = (
            Ether(src=client2_mac, dst=server_mac) 
            / IP(src=client2_ip, dst=server_ip) 
            / TCP(sport=client2_sport, dport=server_port, flags='S')
        )
        writer.write(client2_syn)

        # Server TCP SYN-ACK Packet for Client 2
        server_syn_ack_client2 = (
            Ether(src=server_mac, dst=client2_mac) 
            / IP(src=server_ip, dst=client2_ip) 
            / TCP(sport=server_port, dport=client2_sport, flags='SA')
        )
        writer.write(server_syn_ack_client2)

        # Client 2 TCP ACK Packet
        client2_ack = (
            Ether(src=client2_mac, dst=server_mac) 
            / IP(src=client2_ip, dst=server_ip) 
            / TCP(sport=client2_sport, dport=server_port, flags='A')
        )
        writer.write(client2_ack)

        # Client 2 HTTP GET Request
        client2_get = (
            Ether(src=client2_mac, dst=server_mac) 
            / IP(src=client2_ip, dst=server_ip) 
            / TCP(sport=client2_sport, dport=server_port) 
            / Raw(load="GET /resource.png HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
        )
        writer.write(client2_get)

        # Server HTTP 200 OK Response with PNG Data
        server_png_response = (
            Ether(src=server_mac, dst=client2_mac) 
            / IP(src=server_ip, dst=client2_ip) 
            / TCP(sport=server_port, dport=client2_sport) 
            / Raw(load="HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n".encode() + b'\x89PNG\r\n...')
        )
        writer.write(server_png_response)

if __name__ == "__main__":
    create_pcapng("challenge.pcapng")
