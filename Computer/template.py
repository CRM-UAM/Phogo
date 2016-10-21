#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

from crmphogo import *

from shapes import star, koch_flake

##################################################

pen_down()
forward()
back()
right()
left()
d = obstacle()
print(d)
pen_up()


#star(5, 3, 30)
