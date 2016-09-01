#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import bluetooth

import selectors

try:
    import bluetooth as bt
except ImportError:
    print("PyBluez must be installed.")
    print("You can get it by typing the following command 'pip3 install pybluez' in your shell")
    sys.exit(1)

def receive(sock, mask):
    data = ''
    while not data.endswith('\n'):
        data += sock.recv(1024).decode("utf-8")
    data = data.strip()
    print(data)

MAC = "B4:9D:0B:4C:D9:8D"

sock = bt.BluetoothSocket(bt.RFCOMM)
sock.connect((MAC, 1))
sock.settimeout(None)

sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, receive)

try:
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
except KeyboardInterrupt:
    sock.close()
