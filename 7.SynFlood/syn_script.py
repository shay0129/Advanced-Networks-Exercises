from scapy.all import rdpcap, IP, TCP
from collections import defaultdict
import ipaddress

def read_ips_from_file(file_path):
    """
    Reads IP addresses from a file and returns them as a set.

    Args:
        file_path (str): Path to the file containing IP addresses.

    Returns:
        set: A set of IP addresses read from the file.
    """
    try:
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return set()
    except PermissionError:
        print(f"Error: Permission denied to read the file {file_path}.")
        return set()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return set()

def identify_attackers(pcap_file, attackers_list_file, attacked_network_range, syn_threshold=5, time_window=60):
    try:
        # Read the pcap file
        packets = rdpcap(pcap_file) 
    except FileNotFoundError:
        print(f"Error: The file {pcap_file} was not found.")
        return
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    known_attackers = read_ips_from_file(attackers_list_file)
    # Convert attacked_network_range to an ip_network object
    attacked_network = ipaddress.ip_network(attacked_network_range, strict=False)

    # Dictionary to store the count of SYN packets per IP
    ip_count = defaultdict(int) 
    ip_timestamps = defaultdict(list)  

    for pkt in packets:
        if TCP in pkt and IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

            # Filter based on destination IP, not source IP
            if not ipaddress.ip_address(dst_ip) in attacked_network:  # fixed line
                continue
            if pkt[TCP].flags == 'S':
                ip_count[src_ip] += 1
                ip_timestamps[src_ip].append(pkt.time)

    # Identify suspicious IPs based on the SYN packet count and timestamp analysis
    suspected_attackers = set()
    for ip, count in ip_count.items():
        if count > syn_threshold:
            timestamps = ip_timestamps[ip]
            if max(timestamps) - min(timestamps) <= time_window:
                suspected_attackers.add(ip)

    # Compare with known attackers
    detected_attackers = suspected_attackers
    missing_attackers = known_attackers - detected_attackers
    excess_attackers = detected_attackers - known_attackers
    
    print(f"Missing IP addresses: {missing_attackers}")
    print(f"Additional IP addresses: {excess_attackers}")
    print(f"Attacker IP addresses have been saved to 'attackers_ips.txt'.")

    # Write the detected attacker IPs to a file
    try:
        with open('attackers_ips.txt', 'w') as f:
            for ip in detected_attackers:
                f.write(f"{ip}\n")
    except IOError as e:
        print(f"Error writing to file 'attackers_ips.txt': {e}")

if __name__ == "__main__":
    pcap_file_path = "SYNflood.pcapng"
    attackers_list_file = "attackersListFiltered.txt"
    attacked_network_range = "100.64.0.0/16"
    
    identify_attackers(pcap_file_path, attackers_list_file, attacked_network_range)
