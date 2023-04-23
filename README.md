# NTP-Amplification
Tool for NTP-Amplification attack. It uses the pools specified in the *config.json* to scan for public ntp-servers, these servers will be used to attack the specified target.

![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![version](https://img.shields.io/badge/version-1.0-lightgrey.svg)

## Disclaimer
**This tool is designed for educational purposes only, i do not support the use for any illegal activities.
Only use this on networks you own or have permission for.**

## Requirements

**Install Scapy and ntp**
```
sudo apt install python3-scapy && sudo apt install ntp
```
## Usage
**Example**
```
sudo python3 ntp_amplification.py 192.168.2.1
```