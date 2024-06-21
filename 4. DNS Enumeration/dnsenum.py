# dnsenum.py - Part C: Enumerate DNS servers for a domain using Scapy

from scapy.all import IP, UDP, DNS, DNSQR, sr1, DNSRR
import sys

# List of Subdomains
subdomains = [
    "mail", "cc", "01", "02", "03", "04", "05", "06", "07", "08", "09", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "aa", "ab", "ac", "access", "accounting", "accounts", "ad", "admin", "administrator", "ae", "af", "ag", "ah", "ai", "aix", "aj", "ak", "al", "am", "an", "ao", "ap", "apollo", "aq", "ar", "archivos", "as", "at", "au", "aula", "aulas", "av", "aw", "ax", "ay", "ayuda", "az",
    "b", "ba", "backup", "backups", "bart", "bb", "bc", "bd", "be", "beta", "bf", "bg", "bh", "bi", "biblioteca", "billing", "bj", "bk", "bl", "blackboard", "blog", "blogs", "bm", "bn", "bo", "bp", "bq", "br", "bs", "bsd", "bt", "bu", "bv", "bw", "bx", "by", "bz",
    "c", "ca", "cache", "cadastro", "cal", "calendar", "cam", "canal", "capacitacion", "car", "catalog", "catalogo", "cd", "ce", "cel", "celular", "celulares", "cf", "cg", "ch", "chat", "ci", "ciber", "ciclo", "cine", "cisco", "cj", "ck", "cl", "class", "classroom", "clientes", "cm", "cn", "co", "cobranza", "com", "comercial", "compras", "computo", "config", "configuracion", "connect", "contact", "contacto", "content", "correo", "cp", "cq", "cr", "cs", "ct", "cu", "cv", "cw", "cx", "cy", "cz",
    "d", "da", "db", "dc", "dd", "de", "demo", "departamentos", "design", "dev"
]

def get_dns_query(domain_name):
    """
    Creates a DNS query packet for the specified domain name.
    """
    dns_query = IP(dst='8.8.8.8') / \
                UDP(sport=56385, dport=53) / \
                DNS(rd=1, qd=DNSQR(qname=domain_name, qtype='A'))
    return dns_query

def get_authoritative_dns(domain):
    """
    Retrieves the authoritative DNS server for the domain.
    """
    response = sr1(IP(dst='8.8.8.8') / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype='NS')), timeout=2, verbose=0)
    if response and response.haslayer(DNS) and response[DNS].ancount > 0: # Check if response contains DNS records
        rdata = response[DNS].an[0].rdata
        if isinstance(rdata, bytes):
            return rdata.decode()
        elif isinstance(rdata, str):
            return rdata  # Just return the string as is if it's already a string
    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python dnsenum.py <domain>")
        return  # Don't exit, just return from the function

    domain_name = sys.argv[1]

    # Get the authoritative DNS server for the domain
    authoritative_dns = get_authoritative_dns(domain_name)
    if not authoritative_dns:
        print(f"Failed to get authoritative DNS server for {domain_name}")
        return  # Don't exit, just return from the function
    
    print(f"Authoritative DNS server for {domain_name}: {authoritative_dns}")

    for subdomain in subdomains: # Iterate over each subdomain
        full_domain = f"{subdomain}.{domain_name}"
        query = get_dns_query(full_domain)
        
        # Send the DNS query packet and receive a response
        response = sr1(query, verbose=0)  # sr1 to get single response, verbose=0 for silent mode
        
        # Check if response is not None and has DNS Resource Records (DNSRR)
        if response and response.haslayer(DNSRR):
            print(f"Name:    {full_domain}")
            for i in range(response[DNS].ancount):  # Iterate over each DNS Resource Record (DNSRR)
                if response[DNSRR][i].type == 1:  # Check if it's an IPv4 address (A record)
                    print(f"IP Address:  {response[DNSRR][i].rdata}")       

if __name__ == "__main__":
    main()

"""
Foundations of Network Security and Penetration Testing:

    Name:    mail.jct.ac.il
    IP Address:  147.161.1.38
    IP Address:  147.161.1.36
    IP Address:  147.161.1.29

    Name:    cc.jct.ac.il
    IP Address:  147.161.1.49

    Name:    backup.jct.ac.il
    IP Address:  10.1.101.1

    Name:    bi.jct.ac.il
    IP Address:  10.1.11.44

    Name:    ca.jct.ac.il
    IP Address:  10.1.12.100
"""