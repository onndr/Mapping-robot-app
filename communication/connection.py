from threading import Thread
import socket


class SendingDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ReceivingDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ReceiveThreadUnavaibleError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IncomingMessageSubscriber():
    def __init__(self):
        pass

    def update(self, messages):
        pass


class BluetoothSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM,
                                    socket.BTPROTO_RFCOMM)
        self.connected_to = None
        self.subscribers = []
        self.received_data = []
        self.sent_data = []
        self.recv_thread = None

    def run_recv_thread(self, recv_buf_size: int = 8192):
        self._run_recv_thread = True
        def target():
            while self._run_recv_thread:
                if self.connected_to:
                    data = self.recv(recv_buf_size)
                    # if data:
                    #     print(f"Received chunk: {data}")
            self.close()

        self.recv_thread = Thread(target=target)
        self.recv_thread.start()

    def stop_recv_thread(self):
        self._run_recv_thread = False

    def connect(self, device_mac_address: str, port: int):
        try:
            self.socket.connect((device_mac_address, port))
            self.connected_to = (device_mac_address, port)
            print("Bluetooth connection successful!")
        except Exception as e:
            print(f"Bluetooth connection failed. The encountered error: {e}")

    def send(self, data: str):
        try:
            if self.connected_to:
                self.socket.send(bytes(data, 'UTF-8'))
                self.sent_data.append(data)
            else:
                raise SendingDataError(f"Error. No connected device")
        except Exception as e:
            raise SendingDataError(f"Error sending {data} to {self.connected_to[0]}:{self.connected_to[1]}")

    def recv(self, nbytes: int = 1024):
        try:
            if self.connected_to:
                data = self.socket.recv(nbytes).decode("ascii")
                self.received_data.append(data)
                self.notify_subscribers()
                return data
            else:
                raise ReceivingDataError(f"Error. No connected device")
        except Exception as e:
            raise ReceivingDataError(f"Error receiving data from {self.connected_to[0]}:{self.connected_to[1]}")

    def close(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM,
                                    socket.BTPROTO_RFCOMM)


    def subscribe(self, subscriber: IncomingMessageSubscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: IncomingMessageSubscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self):
        for s in self.subscribers:
            s.update(self.received_data[-1])
