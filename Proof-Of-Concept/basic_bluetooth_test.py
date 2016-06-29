# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

import bluetooth
import time

mac = "B4:9D:0B:4C:D9:8D"

program = "PD\nFD 10\nPU\n"

BT_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

print("Connecting to robot with MAC: " + mac)
BT_socket.connect((mac, 1))  # port=1
BT_socket.settimeout(1)
print("Connected")

time.sleep(4)
print("Sending program:")
print(program)
BT_socket.send(program)

time.sleep(5)
BT_socket.close()

