from ..connection import BluetoothSocket
import sys
import tests_defaults

sensor_address = tests_defaults.DEFAULT_BT_MAC
port = tests_defaults.DEFAULT_BT_PORT
payload = "run"

# test_comm.py MAC PORT PAYLOAD
argc = len(sys.argv)
if argc > 1:
    sensor_address = sys.argv[1]
if argc > 2:
    port = sys.argv[2]
if argc > 3:
    payload = sys.argv[3]

socket = BluetoothSocket()

try:
    socket.connect(sensor_address, int(port))
    print("Bluetooth connection successful!")
    print(f"Trying to send: {payload}")
    socket.send(payload.encode("ascii"))
    print(f"The chunk was sent: {payload}")
except Exception as e:
    print(f"The encountered error: {e}")
finally:
    socket.close()
