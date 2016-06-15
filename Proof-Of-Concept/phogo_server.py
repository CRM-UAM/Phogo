# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

import bluetooth
import time

# sudo /etc/init.d/bluetooth restart

robot = dict()


def add_new_robot(id, mac_address):
    robot[id] = dict()
    robot[id]["mac_address"] = mac_address
    robot[id]["status"] = "Uninitialized"
    robot[id]["socket"] = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

add_new_robot(1, '98:D3:31:B2:DD:F9')
add_new_robot(2, '98:D3:31:20:1A:4B')
add_new_robot(3, '98:D3:31:20:1A:58')


def is_connected(id):
    try:
        robot[id]["socket"].send("test")
    except:
        return False
    return True


def maintain_bluetooth_connection(id):
    if is_connected(id):
        return
    robot[id]["status"] = "Uninitialized"
    BT_socket = robot[id]["socket"]
    print("Connecting to robot " + str(id) +
          ", MAC: " + robot[id]["mac_address"])
    try:
        BT_socket.connect((robot[id]["mac_address"], 1))  # port=1
        BT_socket.settimeout(2)
        print("Connected")
        robot[id]["status"] = "Connected"
    except:
        print("ERROR: Could not connect")
        BT_socket.close()
    robot[id]["socket"] = BT_socket

while(True):
    for id in robot.keys():
        maintain_bluetooth_connection(id)
        maintain_socket_connection(id)

        read_from_socket(id)
        send_to_bluetooth(id)

        read_from_bluetooth(id)
        send_to_socket(id)
