# DISCLAIMER: For educational use only. Only scan networks you own or have permission to test.
import socket
import threading
from datetime import datetime

lock = threading.Lock()
open_ports = []

def grab_banner(ip, port):
    """Try to grab the service banner from an open port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        
        # Send a probe to trigger a banner response
        if port == 80 or port == 443:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        elif port == 22:
            s.send(b"SSH-2.0-OpenSSH\r\n")
        else:
            s.send(b"\r\n")
        
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        
        if banner:
            # Clean up the banner (take only the first line)
            first_line = banner.split("\n")[0].strip()
            return first_line
    except:
        pass
    return "Unknown Service"

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            banner = grab_banner(ip, port)
            with lock:
                print(f"[+] Port {port:5d} OPEN  -> {banner}")
                open_ports.append((port, banner))
        s.close()
    except:
        pass

def main():
    print("=== Simple Port Scanner with Banner Grabbing ===")
    
    target = input("Enter target IP or hostname: ")
    
    try:
        ip = socket.gethostbyname(target)
        print(f"[*] Target IP: {ip}\n")
    except:
        print("[-] Cannot resolve hostname")
        return
    
    port_range = input("Enter port range (e.g., 1-1000): ")
    if "-" in port_range:
        start, end = map(int, port_range.split("-"))
    else:
        start, end = 1, int(port_range)
    
    print(f"[*] Scanning ports {start}-{end}")
    print(f"[*] Started: {datetime.now()}\n")
    
    ports = list(range(start, end + 1))
    
    while ports:
        chunk = ports[:50]
        ports = ports[50:]
        threads = []
        for p in chunk:
            t = threading.Thread(target=scan_port, args=(ip, p))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    
    print(f"\n[*] Scan completed: {datetime.now()}")
    print(f"\n=== Results ===")
    if open_ports:
        for port, banner in open_ports:
            print(f"Port {port}: {banner}")
    else:
        print("No open ports found.")
    
    # Save to file
    with open("scan_results.txt", "w") as f:
        f.write(f"Target: {ip}\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Total open ports: {len(open_ports)}\n\n")
        for port, banner in open_ports:
            f.write(f"Port {port}: {banner}\n")
    
    print(f"\n[*] Results saved to scan_results.txt")

if __name__ == "__main__":
    main()
