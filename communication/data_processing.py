from .data_block import MeasurementsDataBlock
from .connection import IncomingMessageSubscriber


class ProcessedDataSubscriber():
    def __init__(self):
        pass

    def update(self, data_block:MeasurementsDataBlock):
        pass


class DataProcessor(IncomingMessageSubscriber):
    DATA_HEADER = "2"
    STATUS_HEADER = "status:"

    def __init__(self, packets_queue_len = 5):
        self.subscribers = []
        self.data_blocks = []
        self.packet_buf = ""

    def subscribe(self, subscriber: ProcessedDataSubscriber):
        self.subscribers.append(subscriber)

    def update(self, messages: str):
        self.packet_buf += messages
        if ";" in self.packet_buf:
            msg, tail = self.packet_buf.split(";", maxsplit=1)
            self.packet_buf = tail
            self.parse_message(msg)

    def parse_message(self, message: str):
        # data message should look like "2, int, int, int, int"
        data = message.split(",")
        if data[0] != self.DATA_HEADER or len(data) != 5:
            return
        # unpack floats from fixed point representation
        x, y, rotation = [0.001 * float(x) for x in data[1:4]]
        distance = int(data[4])
        self.data_blocks.append(
            MeasurementsDataBlock(x, y, rotation, distance))

        self.notify_subscribers()

    def notify_subscribers(self):
        for s in self.subscribers:
            s.update(self.data_blocks[-1])
