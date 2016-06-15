# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain
from __future__ import print_function  # python2 compatibility

import crmphogo.tortoise as crm
from os.path import dirname

__logo_source = "http://www.ascii-code.com/ascii-art/animals/reptiles/turtles.php"
turtle =r'''
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
       ~-----||====/~     |==================|       |/~~~~~
        (_(__/  ./     /                    \_\      \.
               (_(___/                         \_____)_)
                              PHOGO
                             CRM-UAM
'''
print(turtle)

tortoise = crm.Tortoise(dirname(crm.__file__) + "/robot_bt_mac.txt")

# define the wrappers
EmpezarADibujar = tortoise.start_drawing
DejarDeDibujar = tortoise.stop_drawing
Avanzar = tortoise.forward
Retroceder = tortoise.backward
GirarDerecha = tortoise.turn_right
GirarIzquierda = tortoise.turn_left

# and export them
__all__ = ['EmpezarADibujar', 'DejarDeDibujar', 'Avanzar',
           'Retroceder', 'GirarDerecha', 'GirarIzquierda']
