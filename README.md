# NTP-Amplification
Tool for NTP-Amplification attack. It uses the pools specified in the *config.json* to scan for public ntp-servers, these servers will be used to attack the specified target.

## Disclaimer
**This tool is designed for educational purposes only, i do not support the use for any illegal activities.
Only use this on networks you own or have permission for.**

## Requirements
**Install Scapy**
```
sudo apt-get install python3-scapy
```
## Usage
**Example**
```
python3 ntp_amplification.py 192.168.2.1
```