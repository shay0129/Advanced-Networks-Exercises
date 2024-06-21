# recieve_dns_response.py - Part B: Receive and display the SOA record from a DNS server using Scapy

from scapy.all import DNS, sr1
from dnsenum import get_soa_query

domain_name = 'jct.ac.il'
def main():

    soa_query = get_soa_query(domain_name)

    #Send the DNS query packet and receive a response
    response = sr1(soa_query, timeout=2, verbose=0)  # timeout=2 seconds, verbose=0 to suppress output initially
    if response is not None:
        print("Received DNS response:")
        #response.show()  # Display the response details

        # Check if the response contains an SOA record in the 'ns' section
        if response.haslayer(DNS) and response[DNS].nscount > 0:
            for i in range(response[DNS].nscount):
                if response[DNS].ns[i].type == 6:  # Check if the record is of type SOA
                    mname = response[DNS].ns[i].mname.decode()  # Extract and decode the mname
                    print("Primary name server (mname):", mname)
    else:
        print("No response received from DNS server.")

if __name__ == "__main__":
    main()