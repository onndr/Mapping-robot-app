import random
from ..connection import BluetoothSocket
from time import sleep
import sys
import tests_defaults

sensor_address = tests_defaults.DEFAULT_BT_MAC
port = tests_defaults.DEFAULT_BT_PORT

# test_comm.py MAC PORT
argc = len(sys.argv)
if argc > 1:
    sensor_address = sys.argv[1]
if argc > 2:
    port = sys.argv[2]

socket = BluetoothSocket()

try:
    socket.connect(sensor_address, int(port))
    socket.run_recv_thread()
    print("Bluetooth connection successful!")
    commands = ["run", "stop"]
    while True:
        payload = random.choice(commands)
        print(f"Trying to send: {payload}")
        socket.send(payload.encode("ascii"))
        print(f"The chunk was sent: {payload}")
        sleep(1)
except Exception as e:
    print(f"The encountered error: {e}")
finally:
    socket.close()
