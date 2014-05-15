#!/usr/bin/env python

import re
import subprocess

ARP = "arp"
IP = "10.2.0.87"
CMD = "%s %s" %(ARP, IP)
macPattern = re.compile(":")

def getMac():
    p = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.read()
    result = out.split()
    for chunk in result:
        if re.search(macPattern, chunk):
            return chunk

if __name__ == "__main__":
    macAddr = getMac()
    print macAddr
