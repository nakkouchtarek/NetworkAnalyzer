from scapy.all import *
import socket
from socket import getservbyport
import time
import sys
import os


class ClientSniffer:
    ip_first_three = "192"

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
        self.socket.connect((self.address, self.port))

    def check_if_addr_exists(self, addr, packet):
        if addr in self.adds and str(addr)[:3] == ClientSniffer.ip_first_three:
            value = self.connections[addr]

            self.connections[addr] = int(value) + 1
            buffer = self.size[addr]
            self.size[addr] = int(buffer) + int(len(packet))
            self.total += 1
        else:
            if str(addr)[:3] == ClientSniffer.ip_first_three:
                self.adds.append(addr)
                self.size[addr] = len(packet)
                self.connections[addr] = 1
                self.total += 1

    def get_protocol(self, pkt):
        try:
            if getservbyport(int(pkt.dport)) or getservbyport(int(pkt.sport)):
                try:
                    _proto = getservbyport(int(pkt.dport))
                    return _proto
                except:
                    _proto = getservbyport(int(pkt.dport))
                    return _proto
        except:
            proto_field = pkt[IP].get_field('proto')
            _proto = proto_field.i2s[pkt[IP].proto]
            return _proto

    def check_if_packet_exists(self, packet):
        try:
            name = self.get_protocol(packet)
            if name in self.protos:
                value = self.packets[name]
                self.packets[name] = int(value) + 1
                self.proto_total += 1
            else:
                self.protos.append(name)
                self.packets[name] = 1
                self.proto_total += 1
        except:
            pass

    def handle_packet(self, packet):
        try:
            self.check_if_addr_exists(packet[IP].src, packet)
            self.check_if_addr_exists(packet[IP].dst, packet)
            self.check_if_packet_exists(packet)
            proto = self.get_protocol(packet)
            to_send = f'{packet[IP].src};{packet[IP].dst};{proto};{len(packet)};{packet.summary()}'
            self.socket.send(str(to_send).encode())
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
                print("\n *** ADDRESSES => % OF DATA SENT/RECEIVED IN TOTAL *** ")
                for key3 in self.size:
                    print(key3, '->', self.size[key3], end='\n')
                time.sleep(0.25)

                if os.name == 'nt':
                    os.system("cls")
                else:
                    os.system("clear")
            except:
                pass

    def sniff_packets(self):
        sniff(prn=self.handle_packet)

    def main(self):
        Thread(target=self.sniff_packets,).start()
        Thread(target=self.update,).start()


addr = sys.argv[1]
port = int(sys.argv[2])
c = ClientSniffer(addr, port)
c.main()
