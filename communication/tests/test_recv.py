from ..connection import BluetoothSocket
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
    socket.connect_to(sensor_address, int(port))
    print("Bluetooth connection successful!")
    data = socket.recv(1024)
    print(f"Received chunk: {data}")
except Exception as e:
    print(f"The encountered error: {e}")
finally:
    socket.close()
