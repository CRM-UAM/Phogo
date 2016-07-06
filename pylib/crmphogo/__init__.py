# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain
from __future__ import print_function  # python2 compatibility

import re
import getpass

from os.path import dirname

_test_robot = '3'

logged_as = getpass.getuser()
user = re.search(r'\d+$', logged_as)
# para testear usamos un robot en concreto, sin depender del usuario
user = user.group() if user else _test_robot

import json
with open(dirname(__file__) + "/all_robots.json", "r") as rbts:
    macs = json.loads(rbts.read())

print("Using robot:", user, "{{{}}}".format(macs[user]))

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
        (_(__/  ./     /                    \_\      \.
               (_(___/                         \_____)_)
                              PHOGO
                             CRM-UAM
'''
print(turtle)

#tortoise = crm.Tortoise(dirname(crm.__file__) + "/robot_bt_mac.txt")
tortoise = crm.Tortoise(macs[user])

# define the wrappers
simulated = tortoise.simulated
real = tortoise.real

pendown = tortoise.pendown
penup = tortoise.penup
forward = tortoise.forward
backward = tortoise.backward
right = tortoise.right
left = tortoise.left
distance = tortoise.read_sensor

# and export them
__all__ = ['simulated', 'real', 'pendown', 'penup',
           'forward', 'backward', 'right', 'left', 'distance']
