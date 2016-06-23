#!/bin/python3.4
# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain
from crmphogo import *

#################################################
#                                               #
#       WRITE CODE FROM THIS BLOCK ONWARDS      #
#                                               #
#################################################

d = LeerSensor()
print(d)
EmpezarADibujar()
DejarDeDibujar()
Avanzar()
Retroceder()
GirarDerecha()
GirarIzquierda()


# se puede hacer que las ordenes se almacenen
# en un buffer y se manden secuencialmente
# al ejecutar la ultima linea 'EjecutarPrograma'
#    - hay una instruccion mas
#    - hay un buffer
# o ir mandando las ordenes segun se ejecutan
#    - mantener abierto el socket (servidor DEP)
