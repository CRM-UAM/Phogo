# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

import bluetooth
import time

# sudo /etc/init.d/bluetooth restart

robot = dict()

def add_new_robot(id,mac_address):
    robot[id] = dict()
    robot[id]["mac_address"] = mac_address
    robot[id]["status"] = "Uninitialized"

add_new_robot(1,'98:D3:31:B2:DD:F9')
add_new_robot(2,'98:D3:31:20:1A:4B')
add_new_robot(3,'98:D3:31:20:1A:58')

def upload_program_to_robot(id, program):
    BT_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print("Connecting to robot "+str(id)+", MAC: "+robot[id]["mac_address"])
    try:
        BT_socket.connect((robot[id]["mac_address"], 1)) # port=1
        BT_socket.settimeout(1)
        print("Connected")
        time.sleep(2)
        print("Sending program:")
        print(program)
        BT_socket.send(program)
        time.sleep(2)
        BT_socket.close()
    except:
        print("ERROR: Could not connect")
        BT_socket.close()

def led(on):
    if on:
        return "l1\n"
    return "l0\n"

def delay(ms):
    return "p"+str(ms)+"\n"

def blink(n=2,ms=100):
    res = ""
    for i in xrange(n):
        res += led(1)
        res += delay(ms)
        res += led(0)
        res += delay(ms)
    return res

while(True):
    for id in robot.keys():
        upload_program_to_robot(id, program=blink(n=id,ms=100)+delay(1000)+blink(n=1,ms=500))
        time.sleep(2)

