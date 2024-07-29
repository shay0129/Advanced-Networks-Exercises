# create_soa_query.py - Part A: Create a DNS query for an SOA record using Scapy

from scapy.all import IP, UDP, DNS, DNSQR, sr1, sniff

def filter_soa_queries(packet):
    # Check if the packet has DNS and DNSQR layers and if it's an SOA query
    return DNS in packet and DNSQR in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype == 6

def print_query_name(dns_packet):
    # Print the query name if the packet has DNS and DNSQR layers
    print(dns_packet[DNSQR].qname.decode())

def print_domain(packet):
    if DNS in packet and DNSQR in packet:
        if packet[DNS].opcode == 0 and packet[DNSQR].qtype == 6:
            print(packet[DNSQR].qname.decode())
            return True
    return False

def main():
    print("waiting....\n")
    # Capture and store packets, then print the first one's details
    # Commented out for now to avoid running this part of the code immediately
    p = sniff(count=1, lfilter=filter_soa_queries, prn=print_domain)
    print(p[0].command())
    print("done")

if __name__ == "__main__":
    main()

