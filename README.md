# Port Scanner with Banner Grabbing

A multi-threaded TCP port scanner written in Python. Scans a target IP or hostname, detects open ports, and grabs service banners to identify what’s running.

### ⚠️ Legal & Ethical Disclaimer
This tool is for educational purposes and authorized security testing only. 
**Do NOT scan networks, IPs, or systems you do not own or have explicit written permission to test.** 
Unauthorized port scanning may violate local laws, computer crime acts, and your ISP’s terms of service. 
The author is not responsible for misuse.

### Features
- **Multi-threaded**: Scans 50 ports concurrently for speed
- **Banner Grabbing**: Identifies services on HTTP, SSH, and other common ports
- **Hostname Resolution**: Accepts both IP addresses and domain names
- **Results Export**: Automatically saves findings to `scan_results.txt`
- **Clean Output**: Shows port number and detected service banner

### Requirements
- Python 3.x
- No external libraries needed - uses `socket`, `threading`, `datetime` from standard library

### Usage
1. Run the script:
   ```bash
   python scanner.py
