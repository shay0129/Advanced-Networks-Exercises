import os

def check_file_inclusion(suspected_ips_file, detected_ips_file):
    """
    Checks if all lines in the first file (suspected IP addresses) are also present in the second file (detected IP addresses).

    Args:
        suspected_ips_file (str): Path to the file containing the list of suspected IP addresses.
        detected_ips_file (str): Path to the file containing the list of detected IP addresses.
    """
    
    try:
        # Get absolute paths to ensure correct file access
        suspected_ips_file = os.path.abspath(suspected_ips_file)
        detected_ips_file = os.path.abspath(detected_ips_file)

        with open(suspected_ips_file, 'r') as f1:
            suspected_ips = set(line.strip() for line in f1)

        with open(detected_ips_file, 'r') as f2:
            detected_ips = set(line.strip() for line in f2)

        missing_ips = suspected_ips - detected_ips
        if missing_ips:
            print("Suspected IP addresses that were not detected:")
            for ip in missing_ips:
                print(ip)
        else:
            print("All suspected IP addresses were successfully detected!")

    except FileNotFoundError as e:
        print(f"Error: The file {e.filename} was not found.")
    except PermissionError as e:
        print(f"Error: Permission denied to read the file {e.filename}.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    file1_path = "7.SynFlood/attackers_ips.txt" 
    file2_path = "7.SynFlood/attackersListFiltered.txt"

    check_file_inclusion(file1_path, file2_path)

