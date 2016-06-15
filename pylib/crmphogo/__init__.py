# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain
# -.- coding: utf-8 -.-
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

t = crm.Tortoise(dirname(crm.__file__) + "/robot_bt_mac.txt")

# define the wrappers
EmpezarADibujar = t.start_drawing
DejarDeDibujar = t.stop_drawing
Avanzar = t.forward
Retroceder = t.backward
GirarDerecha = t.turn_right
GirarIzquierda = t.turn_left

# and export them
__all__ = ['EmpezarADibujar', 'DejarDeDibujar', 'Avanzar',
           'Retroceder', 'GirarDerecha', 'GirarIzquierda']
