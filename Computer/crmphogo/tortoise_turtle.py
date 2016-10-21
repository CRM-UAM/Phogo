# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

# python2 compatibility
from __future__ import print_function

from random import randint
import turtle


def Turtle(*args, **kwargs):
    return _Turtle(*args, **kwargs)


class _Turtle(object):

    def __init__(self):
        turtle.title('Phogo - CRM UAM')
        turtle.mode('logo')
        turtle.penup()

        #turtle.setx(turtle.screensize()[0] // 8)
        turtle.screensize(4000, 4000)

    def command(self, command):
        cmd = command.split()
        if len(cmd) > 1:
            cmd, units = cmd[0], cmd[1]
        else:
            cmd = cmd[0]

        if cmd == 'PD':
            return self._PD()
        elif cmd == 'PU':
            return self._PU()
        elif cmd == 'FD':
            return self._FD(int(units) * 3)
        elif cmd == 'BK':
            return self._BK(int(units) * 3)
        elif cmd == 'RT':
            return self._RT(int(units))
        elif cmd == 'LT':
            return self._LT(int(units))
        elif cmd == 'OE':
            return self._OE()
        else:
            return 'ERROR: UNKNOWN COMMAND'

    def _PD(self):
        turtle.pendown()
        return 'OK'

    def _PU(self):
        turtle.penup()
        return 'OK'

    def _FD(self, units=10):
        turtle.forward(units)
        return 'OK'

    def _BK(self, units=10):
        turtle.backward(units)
        return 'OK'

    def _RT(self, deg=90):
        turtle.right(deg)
        return 'OK'

    def _LT(self, deg=90):
        turtle.left(deg)
        return 'OK'

    def _OE(self):
        return randint(10, 300)
