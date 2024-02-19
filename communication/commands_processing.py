from .connection import BluetoothSocket


class PackageBuilder():
    def create_package(payload: str):
        return payload + ";"


class InvalidCommandError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CommandProcessor():
    RUN_CMD = "run"
    STOP_CMD = "stop"
    SHUTDOWN_CMD = "shutdown"
    STATUS_CMD = "status"
    commands = [RUN_CMD, STOP_CMD, SHUTDOWN_CMD, STATUS_CMD]

    def __init__(self):
        pass

    def handle_command(self, socket: BluetoothSocket, command: str):
        if command in self.commands:
            socket.send(PackageBuilder.create_package(command))
        else:
            raise InvalidCommandError(f"The command {command} is not allowed")

    def handle_run_command(self, socket: BluetoothSocket):
        socket.send(PackageBuilder.create_package(self.RUN_CMD))

    def handle_stop_command(self, socket: BluetoothSocket):
        socket.send(PackageBuilder.create_package(self.STOP_CMD))

    def handle_shutdown_command(self, socket: BluetoothSocket):
        socket.send(PackageBuilder.create_package(self.SHUTDOWN_CMD))

    def handle_status_command(self, socket: BluetoothSocket):
        socket.send(PackageBuilder.create_package(self.STATUS_CMD))