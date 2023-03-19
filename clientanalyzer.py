import socket
from psutil import net_io_counters
import time
import os


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776


class ClientSniffer:
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.last_upload, self.last_download = 0, 0
        self.upload_speed, self.down_speed = 0, 0
        self.highest_upload, self.highest_down = 0, 0
        self.lowest_upload, self.lowest_down = 0, 0
        self.socket.connect((self.address, self.port))

    def size(self, B):
        B = float(B)
        if B < KB:
            return f"{B} Bytes"
        elif KB <= B < MB:
            return f"{B/KB:.2f} KB"
        elif MB <= B < GB:
            return f"{B/MB:.2f} MB"
        elif GB <= B < TB:
            return f"{B/GB:.2f} GB"
        elif TB <= B:
            return f"{B/TB:.2f} TB"

    def update(self):
        counter = net_io_counters()

        upload = counter.bytes_sent
        download = counter.bytes_recv
        total = upload + download

        if self.last_upload > 0:
            if upload < self.last_upload:
                self.upload_speed = 0
            else:
                self.upload_speed = upload - self.last_upload

        if self.last_download > 0:
            if download < self.last_download:
                self.down_speed = 0
            else:
                self.down_speed = download - self.last_download

        if self.lowest_down == 0 and self.lowest_upload == 0:
            self.lowest_down = self.down_speed
            self.lowest_upload = self.upload_speed
        else:
            if self.upload_speed < self.lowest_upload:
                self.lowest_upload = self.upload_speed

            if self.upload_speed > self.highest_upload:
                self.highest_upload = self.upload_speed

            if self.down_speed < self.lowest_down:
                self.lowest_down = self.down_speed

            if self.down_speed > self.highest_down:
                self.highest_down = self.down_speed

        self.last_upload = upload
        self.last_download = download

        print(f"Address: {ip}\nUploads: {self.size(upload)}\nDownloads: {self.size(download)}\nUpload Speed: {self.size(self.upload_speed)}\nDownload Speed: {self.size(self.down_speed)}\nHighest download speed: {self.size(self.highest_down)}\nHighest upload speed: {self.size(self.highest_upload)}\nLowest upload speed: {self.size(self.lowest_upload)}\nLowest download speed: {self.size(self.lowest_down)}\n")
        time.sleep(0.25)
        os.system("cls")
        self.socket.send(f"{ip};{self.size(upload)};{self.size(download)};{self.size(total)};{self.size(self.upload_speed)};{self.size(self.down_speed)};{self.size(self.highest_down)};{self.size(self.lowest_down)};{self.size(self.highest_upload)};{self.size(self.lowest_upload)}".encode())

        if self.socket.recv(1024).decode() == "done":
            pass

    def handle_network(self):
        while True:
            try:
                self.update()
            except:
                pass

    def main(self):
        self.handle_network()


addr = input("Address: ")
port = int(input("Port: "))
c = ClientSniffer(addr, port)
c.main()
