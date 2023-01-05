#!/usr/bin/env python3

import subprocess

class NtpServer:
    def __init__(self):
        pass
    
class NtpScanner:
    def __init__(self):
        self.servers = []
        self.pools = []

    def scan(self):
        self.servers.clear()

        output = subprocess.run(["ntpq", "-p"], capture_output=True).stdout.decode()
        for line in output.split("\n"):
            if line.startswith("*") or line.startswith("+"):
                self.servers.append(line.split(" ")[0][1:])

    def addPool(self, pool: str):
        pass

    def removePool(self, pool: str):
        pass

if __name__ == '__main__':
    pass