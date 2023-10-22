import subprocess
import re

# Display a banner at the beginning of the script
print("*********************************************")
print("            Reconnaissance Script            ")
print("*********************************************")

def run_masscan(target_ip):
    print("\nRunning Masscan (requires Sudo)...\n")
    
    masscan_command = f'sudo masscan {target_ip} -p- --rate 4000 -e tun0 | tee masscan_output.txt'

    try:
        subprocess.run(masscan_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Masscan: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_ports_from_masscan_output():
    try:
        with open("masscan_output.txt", "r") as file:
            contents = file.read()
            port_matches = re.findall(r'Discovered open port (\d+)/\w+ on \d+\.\d+\.\d+\.\d+', contents)
            if port_matches:
                return ",".join(port_matches)
    except FileNotFoundError:
        return None

def run_nmap(target_ip):
    ports1 = extract_ports_from_masscan_output()
    if ports1 is not None:
        print(f"\nRunning Nmap scan on {target_ip} for ports: {ports1}...")
        nmap_command = f'sudo nmap -A -p {ports1} -T4 -oA nmap_scan {target_ip} -vv'
        subprocess.run(nmap_command, shell=True)
        print("Nmap scan completed. Results saved to nmap_scan.xml")
    else:
        print("Error reading ports from 'masscan_output.txt': File not found or no valid ports detected.")



def run_gobuster(target_ip, port):
    print(f"\nRunning Gobuster scan on {target_ip}:{port} for directory enumeration...")

    gobuster_command = f'gobuster dir -u {target_ip}:{port} -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -o gobuster_scan.txt -t 25 -q -x php,aspx,txt,asp'

    subprocess.run(gobuster_command, shell=True)

    print("Gobuster scan completed. Results saved to gobuster_scan.txt")

def run_gobuster_subdomains(target_domain):
    print(f"\nRunning Gobuster scan on {target_domain} for subdomain enumeration...")
    gobuster_command = f'gobuster dns -d {target_domain} -w /usr/share/dnsrecon/subdomains-top1mil-20000.txt -o gobuster_subdomains.txt -t 25 -q'
    subprocess.run(gobuster_command, shell=True)
    print("Gobuster subdomain scan completed. Results saved to gobuster_subdomains.txt")

def run_gobuster_vsubdomains(target_domain):
    print(f"\nRunning Gobuster scan on {target_domain} for Vsubdomain enumeration...")
    gobuster_command = f'gobuster vhost -u {target_domain} -w /usr/share/dnsrecon/subdomains-top1mil-20000.txt -o gobuster_vsubdomains.txt -t 25 -q'
    subprocess.run(gobuster_command, shell=True)
    print("Gobuster Vhost subdomain scan completed. Results saved to gobuster_vsubdomains.txt")

def run_gospider(options):
    gospider_command = f"gospider {options}"
    try:
        subprocess.run(gospider_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running GoSpider: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def gospider_menu(target_ip, target_domain):
    print("Welcome to the GoSpider script!")
    choice = input("Choose an option (1 for Proxy Scan, 2 for Site Scan): ")
    use_sitemap = input("Do you want to use the sitemap option? (y/n): ").strip().lower()	
    output_file = input("Enter the output file name (e.g., crawl.txt): ")
    
    concurrent = input("Enter the number of concurrent requests (e.g., 10): ")

    if choice == "1":
        port = input("Enter the port number: ")
        run_gospider(f"-p http://{target_ip}:{port} -o {output_file} -c {concurrent}")
    elif choice == "2":
        gospider_options = f"-s http://{target_domain} -o {output_file} -c {concurrent} -d 0 -w -t 10 --robots -a -r -v"

        if use_sitemap == 'y':
            gospider_options += " --sitemap"

        run_gospider(gospider_options)
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    target_domain = input("Enter the target domain for Gobuster Vhost/subdomain enumeration (e.g., example.com): ")
    use_masscan = input("Do you want to use Masscan Scan? (y/n): ").strip().lower()

    if use_masscan != 'n':
        run_masscan(target_ip)

    skip_nmap = input("Do you want to use Nmap scan? (y/n): ").strip().lower()

    if skip_nmap != 'n':
        run_nmap(target_ip)

    run_gospider_menu = input("Do you want to run the GoSpider menu? (y/n): ").strip().lower()

    if run_gospider_menu == 'y':
        gospider_menu(target_ip, target_domain)

    skip_directory_enum = input("Do you want to use Gobuster directory enumeration? (y/n): ").strip().lower()

    if skip_directory_enum != 'n':
        port = input("Enter the port number: ")
        run_gobuster(target_ip, port)

    skip_subdomain_enum = input("Do you want to use Gobuster subdomain enumeration? (y/n): ").strip().lower()

    if skip_subdomain_enum != 'n':
        run_gobuster_subdomains(target_domain)

    skip_Vsubdomain_enum = input("Do you want to use Gobuster Vhost subdomain enumeration? (y/n): ").strip().lower()

    if skip_Vsubdomain_enum != 'n':
        run_gobuster_vsubdomains(target_domain)

    print("\nReconnaissance completed.")
##whatsupp