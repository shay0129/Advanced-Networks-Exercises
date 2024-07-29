import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from scapy.all import DNS, DNSRR

# Import the main function from dnsenum.py
from dnsenum import main

class TestDNSEnum(unittest.TestCase):

    @patch('dnsenum.sr1')
    def test_dnsenum_main(self, mock_sr1):
        # Define the mock response for sr1
        mock_response = MagicMock()
        mock_response.haslayer.return_value = True
        mock_response[DNS].ancount = 3  # Simulate 3 DNS Resource Records (DNSRR)
        mock_response[DNSRR].an = [
            DNSRR(rrname='mail.jct.ac.il', type=1, rdata='147.161.1.38'),
            DNSRR(rrname='mail.jct.ac.il', type=1, rdata='147.161.1.36'),
            DNSRR(rrname='mail.jct.ac.il', type=1, rdata='147.161.1.29')
        ]
        mock_sr1.return_value = mock_response

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Simulate command-line arguments
        sys.argv = ['dnsenum.py', 'jct.ac.il']

        # Call the main function
        main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Assert the printed output matches the expected format
        expected_output = """Authoritative DNS server for jct.ac.il: None
                            Name:    mail.jct.ac.il
                            IP Address:  147.161.1.38
                            IP Address:  147.161.1.36
                            IP Address:  147.161.1.29
                            """
        
        # Normalize and compare the output
        self.assertMultiLineEqual(captured_output.getvalue().strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
