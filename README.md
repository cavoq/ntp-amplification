# NTP-Amplification
Tool for NTP-Amplification attack. It uses the pools specified in the *config.json* to scan for public ntp-servers, these servers will be used to attack the specified target. You can also pass in a list of ntp-servers yourself.

![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![version](https://img.shields.io/badge/version-1.5.3-lightgrey.svg)
![build](https://img.shields.io/github/actions/workflow/status/cavoq/ntp-amplification/workflow.yml)

## Disclaimer
**This tool is designed for educational purposes only, i do not support the use for any illegal activities.
Only use this on networks you own or have permission for.**

## Note

**Since this script uses scapy, it needs to have root privileges, if
you install it with pip, you need to install it with sudo.**

## Requirements

**System**
```bash
sudo apt update &&
sudo apt install python3-scapy ntp -y
```

## Installation

**PyPi**

```bash
sudo pip install ntp-amplification
sudo ntp-amplification
```

**From source**
```bash
pip install -r requirements.txt
sudo python3 ntp_amplification.py
```

## Usage

```
 _   _ _____ ____         _    __  __ ____  _     ___ _____ ___ _____ ____
| \ | |_   _|  _ \       / \  |  \/  |  _ \| |   |_ _|  ___|_ _| ____|  _ \
|  \| | | | | |_) |____ / _ \ | |\/| | |_) | |    | || |_   | ||  _| | |_) |
| |\  | | | |  __/_____/ ___ \| |  | |  __/| |___ | ||  _|  | || |___|  _ <
|_| \_| |_| |_|       /_/   \_\_|  |_|_|   |_____|___|_|   |___|_____|_| \_\


NTP-Amplification Attack Tool v1.5.3

USAGE: ntp-amplification [options] <target ip>
OPTIONS:
 -h, --help: Show this help message and exit
 -s, --server: Specify ntp server list
 -c, --config: Specify config file
EXAMPLE: ntp-amplification -s example-servers.txt 192.168.2.1

```

## Developer notes

**lint**
```bash
pre-commit run --all-files
```

**test**
```bash
sudo coverage run -m unittest ntp_amplification_test.py
coverage report -m
```

**publish**
```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload --verbose dist/*
```
