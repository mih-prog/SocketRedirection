#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, json

sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send(json.dumps({"password": "tpest"}).encode())
print(sock.recv(1024))
