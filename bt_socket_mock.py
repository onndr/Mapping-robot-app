import random
import time
from communication.connection import *


class BluetoothSocketMock(BluetoothSocket):
    def __init__(self, fragmentation_on=False):
        self.connected_to = None
        self.subscribers = []
        self.received_data = []
        self.sent_data = []
        self.next_data = ""
        self.fragmentation_on = fragmentation_on
        self.run = False

    def generate_fragmentated_data(self):
        if self.next_data:
            send_data = self.next_data
            self.next_data = ""
            return send_data
        data = ["2"] + [str(random.randint(1, 10000)) for i in range(4)]
        t = random.randint(1, 5)
        if t == 5:
            send_data = ",".join(data) + ";"
            self.next_data = ""
        else:
            send_data = ",".join(data[:t]) + ","
            self.next_data = ",".join(data[t:]) + ";"
        return send_data

    def generate_integral_data(self):
        return ",".join(["2"] + [str(random.randint(1, 10000)) for i in range(4)]) + ";"

    def run_recv_thread(self):
        self.run = True
        def target():
            while self.run:
                if self.connected_to:
                    data = self.recv()
                    # print(f"Received chunk: {data}")
                    time.sleep(0.1)

        self.recv_thread = Thread(target=target)
        self.recv_thread.start()

    def connect(self, device_mac_address: str, port: int):
        try:
            self.connected_to = (device_mac_address, port)
            print("Bluetooth connection successful!")
        except Exception as e:
            print(f"Bluetooth connection failed. The encountered error: {e}")

    def send(self, data: str):
        if self.connected_to:
            try:
                # self.socket.send(bytes(data, 'UTF-8'))
                self.sent_data.append(data)
                if "run" in data:
                    self.run_recv_thread()
                if "stop" in data:
                    self.run = False
            except Exception as e:
                raise SendingDataError(f"Error sending {data} to {self.connected_to[0]}:{self.connected_to[1]}")
        else:
            raise SendingDataError(f"Error. No connected device")

    def recv(self, nbytes: int = 1024):
        if self.connected_to:
            try:
                # data = self.socket.recv(nbytes).decode("ascii")
                if self.fragmentation_on:
                    data = self.generate_fragmentated_data()
                else:
                    data = self.generate_integral_data()
                self.received_data.append(data)
            except Exception as e:
                raise ReceivingDataError(f"Error receiving data from {self.connected_to[0]}:{self.connected_to[1]}")

            self.notify_subscribers()
            return data
        else:
            raise ReceivingDataError(f"Error. No connected device")

    def close(self):
        self.connected_to = None

    def subscribe(self, subscriber: IncomingMessageSubscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: IncomingMessageSubscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self):
        for s in self.subscribers:
            s.update(self.received_data[-1])
