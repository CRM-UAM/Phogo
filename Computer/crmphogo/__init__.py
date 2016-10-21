# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain
from __future__ import print_function  # python2 compatibility

import sys
import re
import getpass

from os.path import dirname

_test_robot = '3'

logged_as = getpass.getuser()
user = re.search(r'\d+$', logged_as)
# para testear usamos un robot en concreto, sin depender del usuario
robot = user.group() if user else _test_robot

import json
try:
    with open(dirname(__file__) + "/all_robots.json", "r") as rbts:
        macs = json.loads(rbts.read())
except:
    print("Failed to load configuration file")
    sys.exit(1)

"""yatame"""

mac = macs[robot]
print("Using robot:", robot, "{{{}}}".format(mac))

import crmphogo.tortoise as crm
# __logo_source:
# http://www.ascii-code.com/ascii-art/animals/reptiles/turtles.php
turtle = r'''
                             ___-------___
                         _-~~             ~~-_
                      _-~                    /~-_
   /^\__/^\         /~  \                   /    \
 /|  O|| O|        /      \_______________/        \
| |___||__|      /       /                \          \
|          \    /      /                    \          \
|   (_______) /______/                       \_________ \
|         / /         \                      /            \
 \         \^\\         \                  /               \     /
   \         ||           \______________/      _-_       //\__//
     \       ||------_-~~-_ ------------- \ --/~   ~\    || __/
       ~-----||====/~   /_|==================|       |/~~~~~
        (_(__/   ./    /                    \_\      \.
                (_(___/                        \_____)_)
                              PHOGO
                             CRM-UAM
'''
print(turtle)

#tortoise = crm.Tortoise(dirname(crm.__file__) + "/robot_bt_mac.txt")
tortoise = crm.Tortoise(mac)

# define the wrappers
simulated = tortoise.simulated
real = tortoise.real

pen_down = tortoise.pendown
pen_up = tortoise.penup
forward = tortoise.forward
back = tortoise.backward
right = tortoise.right
left = tortoise.left
obstacle = tortoise.read_sensor

# and export them
__all__ = ['simulated', 'real', 'pen_down', 'pen_up',
           'forward', 'back', 'right', 'left', 'obstacle']
