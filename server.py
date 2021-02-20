#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, threading
import json
PortDict = {'541': {'port': 541, 'isp': True}, '542': {'port': 542, 'isp': True}, '543': {'port': 543, 'isp': True}}


def ClientToServer(client, server):
    while True:
        data = client.recv(1024)
        if not data:
            break
        datastr = data.decode()
        data = datastr.encode()
        print(data)
        server.send(data)


def ClientJoin(client):
    print(type(client))
    data = client.recv(2048)
    if not data:
        return 1
    jsonres = data.decode()
    res = json.loads(jsonres)
    if res.get('password') == 'test':
        port = None
        for key in PortDict:
            if PortDict[key].get('isp'):
                PortDict[key]['isp'] = False
                port = PortDict[key].get('port')
                break
        if port is not None:
            CliServ = socket.socket()
            CliServ.bind(('0.0.0.0', port))
            CliServ.listen(1)
            RecvTred = threading.Thread(target=ClientToServer, args=(CliServ, client))
            SendTread = threading.Thread(target=ClientToServer, args=(client, CliServ))

        else:
            client.send(json.dumps({'error': 'NotFreePort'}).encode())
            client.close()
    else:
        client.send(json.dumps({'error': 'InvalidPassword'}).encode())
        client.close()


sock = socket.socket()
sock.bind(('', 9090))
sock.listen(3)

while True:
    conn, addr = sock.accept()
    UsPr = threading.Thread(target=ClientJoin, args=(conn,))
    UsPr.run()

