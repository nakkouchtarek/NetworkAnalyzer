import socket
from scapy.all import *
from threading import Thread
import sys


class ServerSniffer:
    ip_base = "192.168"

    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.adds = []
        self.protos = []
        self.total = 0
        self.proto_total = 0
        self.total_buffer = 0
        self.connections = {}
        self.packets = {}
        self.size = {}
        self.socket.bind((self.address, self.port))
        self.socket.listen()

    def check_if_addr_exists(self, addr, buffer):
        if addr in self.adds and addr[:7] == ServerSniffer.ip_base:
            value = self.connections[addr]
            self.connections[addr] = int(value) + 1
            _buffer = self.size[addr]
            self.size[addr] = int(_buffer) + int(buffer)
            self.total += 1
        else:
            if addr[:7] == ServerSniffer.ip_base:
                self.adds.append(addr)
                self.size[addr] = int(buffer)
                self.connections[addr] = 1
                self.total += 1

    def check_if_packet_exists(self, proto):
        try:
            if proto in self.protos:
                value = self.packets[proto]
                self.packets[proto] = int(value) + 1
                self.proto_total += 1
            else:
                self.protos.append(proto)
                self.packets[proto] = 1
                self.proto_total += 1
        except:
            pass

    def handle_client(self, client):
        while True:
            data = client.recv(1024).decode()
            if data:
                data = data.split(';')
                try:
                    self.check_if_addr_exists(data[0], data[3])
                    self.check_if_addr_exists(data[1], data[3])
                    self.check_if_packet_exists(data[2])
                    # print(data[2])
                except:
                    pass

    def update(self):
        while True:
            try:
                print("*** ADDRESSES => % OF CONSUMPTION ***")
                for key in self.connections:
                    prctg = (int(self.connections[key]) / self.total) * 100
                    print(key, '->', "%.2f" % prctg + "%"+'\n', end='')
                print("\n*** TYPE OF PACKETS => % OF CONSUMPTION ***")
                for key2 in self.packets:
                    prctg2 = (int(self.packets[key2]) / self.proto_total) * 100
                    print(key2, '->', "%.2f" % prctg2 + "%" + '\n', end='')
                print(
                    "\n *** ADDRESSES => % OF DATA SENT/RECEIVED IN TOTAL IN BYTES *** ")
                for key3 in self.size:
                    print(key3, '->', self.size[key3], end='\n')
                time.sleep(0.25)

                if os.name == 'nt':
                    os.system("cls")
                else:
                    os.system("clear")
                    
            except:
                pass

    def accept_client(self):
        Thread(target=self.update,).start()
        while True:
            try:
                client, addr = self.socket.accept()
                if client:
                    Thread(target=self.handle_client, args=(client,)).start()
            except KeyboardInterrupt:
                exit()


addr = sys.argv[1]
port = int(sys.argv[2])
s = ServerSniffer(addr, port)
s.accept_client()
