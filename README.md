# NTP-Amplification

![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![CI/CD](https://img.shields.io/github/actions/workflow/status/cavoq/ntp-amplification/workflow.yml)
![PyPI version](https://img.shields.io/pypi/v/ntp-amplification)
![Debian Compatible](https://img.shields.io/badge/Debian-Compatible-brightgreen.svg)

This tool performs NTP-Amplification tests using the server pools specified in config.json to locate public NTP servers. These servers can reflect packets toward a specified target. You may also provide your own list of NTP servers. Only run this tool against systems you are authorized to test.

## Disclaimer

**LEGAL NOTICE**: This tool is intended strictly for educational purposes and authorized defensive testing. Unauthorized use against systems you do not own or lack explicit written permission for may be illegal and subject to civil or criminal penalties. The author accepts no responsibility for misuse.

## Note

**Scapy needs root privileges to send packets, therefore this script requires root privileges.**

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


NTP-Amplification Attack Tool v1.7.2

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
coverage report -m --include=ntp_amplification.py
```

**publish**
```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload --verbose dist/*
```
