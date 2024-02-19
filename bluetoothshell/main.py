from communication.commands_processing import CommandProcessor
from communication.connection import BluetoothSocket
from communication.data_processing import DataProcessor, ProcessedDataSubscriber


class BluetoothSub(ProcessedDataSubscriber):
    def update(self, data_block):
        print("new block: ", data_block)


def main():
    bt = BluetoothSocket()
    sub = BluetoothSub()
    processor = DataProcessor()
    cmd_processor = CommandProcessor()
    bt.subscribe(processor)
    processor.subscribe(sub)
    MAC = "00:13:EF:01:11:98"
    port = 1
    bt.connect(MAC, port)
    bt.run_recv_thread()
    while True:
        command = input("command:")
        print("recieved: ", command)
        if command == "exit":
            bt.close()
            break
        cmd_processor.handle_command(bt, command)


if __name__ == "__main__":
    main()
