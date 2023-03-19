import socket
from scapy.all import *
from threading import Thread
import time
import os


class ServerSniffer:
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.socket.bind((self.address, self.port))
        self.socket.listen()

    def handle_client(self, client):
        while True:
            print(f"|     IP ADDRESS    |    UPLOADS     |   DOWNLOADS     |   TOTAL     |   UPLOAD SPEED   |   DOWNLOAD SPEED   |   HIGHEST DOWNLOAD SPEED   |   LOWEST DOWNLOAD SPEED   |   HIGHEST UPLOAD SPEED    |    LOWEST UPLOAD SPEED  |")
            data = client.recv(2048).decode()
            if data:
                data = data.split(';')
                try:
                    print(
                        f"|     {data[0]:15s}      |      {data[1]:10s}     |     {data[2]:10s}     |     {data[3]:10s}     |     {data[4]:10s}     |     {data[5]:10s}     |     {data[6]:10s}     |     {data[7]:10s}     |     {data[8]:10s}      |      {data[9]:10s}    |")
                    client.send("done".encode())
                    time.sleep(0.25)
                    os.system("cls")
                except:
                    pass

    def accept_client(self):
        while True:
            try:
                client, addr = self.socket.accept()
                if client:
                    Thread(target=self.handle_client,
                           args=(client,)).start()
            except:
                pass


addr = input("Address: ")
port = int(input("Port: "))
s = ServerSniffer(addr, port)
s.accept_client()
