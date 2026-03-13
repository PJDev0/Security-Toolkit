import socket
import argparse
import concurrent.futures
import sys

# --- CONFIGURATION ---
# These are color codes to make the terminal look nice
GREEN = "\033[92m"  # Open ports
RED = "\033[91m"    # Errors
RESET = "\033[0m"   # Reset color
BLUE = "\033[94m"   # Information

def scan_port(target, port):
    """
    Scans a single port on the target.
    Returns a tuple (port, status, banner) if open, else None.
    """
    try:
        # Create a socket object (The connection tool)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Wait maximum 1 second for an answer
        
        # Try to connect. 0 means success (Open).
        result = s.connect_ex((target, port))
        
        if result == 0:
            banner = ""
            try:
                # Try to grab the banner (Identify the service)
                # We send a generic HTTP request. If it's not a web server, 
                # it will just ignore it or disconnect.
                s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner_bytes = s.recv(1024)
                
                # We use errors='ignore' so we don't crash if the server sends weird symbols
                banner = banner_bytes.decode(errors='ignore').strip()
            except:
                banner = "No Banner" 
            
            s.close()
            return (port, True, banner)
        
        s.close()
        
    except Exception:
        # Something went wrong (e.g. network error), ignore and continue
        return None

def main():
    # Setup command line arguments (How you use the tool)
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address (e.g., 127.0.0.1)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (e.g., 1-1024) or specific ports (e.g., 80,443)")
    args = parser.parse_args()

    target = args.target
    port_input = args.ports

    print(f"{BLUE}[*] Starting Scan...{RESET}")
    print(f"{BLUE}[*] Target: {target}{RESET}")
    print(f"{BLUE}[*] Ports: {port_input}{RESET}")
    print("-" * 50)

    # Parse the port range (Convert user input '1-100' into a list)
    ports = []
    try:
        if "-" in port_input:
            start, end = map(int, port_input.split("-"))
            # Limit scan to avoid freezing if user types 1-65535 on slow machine
            ports = range(start, min(end + 1, 65536)) 
        else:
            ports = map(int, port_input.split(","))
    except ValueError:
        print(f"{RED}[!] Invalid port format. Use '1-1024' or '80,443'{RESET}")
        sys.exit(1)

    open_ports_count = 0

    # Use ThreadPoolExecutor for multi-threading (Scan fast!)
    # max_workers=100 means it checks 100 ports at the same time.
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Submit all tasks
        futures = [executor.submit(scan_port, target, port) for port in ports]
        
        # Process results as they come in
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                port, is_open, banner = result
                print(f"{GREEN}[+] Port {port} is OPEN{RESET}")
                if banner and banner != "No Banner":
                    print(f"     Banner: {banner}")
                open_ports_count += 1

    print("-" * 50)
    print(f"{GREEN}Scan complete! Found {open_ports_count} open ports.{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Scan interrupted by user (Ctrl+C).{RESET}")
        sys.exit(0)