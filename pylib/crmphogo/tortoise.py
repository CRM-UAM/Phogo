# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain


# python2 compatibility
from __future__ import print_function

import sys
import os
import re

try:
    import bluetooth as bt
except ImportError:
    print("PyBluez must be installed.")
    # sys.exit(1)

try:
    input = raw_input
except:
    pass


class TortoiseError(Exception):
    pass


class _TortoiseBT(object):
    """docstring for TortoiseBT"""

    def __init__(self, host):
        self.bt_socket = bt.BluetoothSocket(bt.RFCOMM)
        self._host = host
        self._connected = False

    def _connect(self):
        if not self._connected:
            for i in range(3):  # we try to connect 3 times at most
                try:
                    self.bt_socket.connect((self._host, 1))
                except bt.BluetoothError as bte:
                    print('Intento ({}) de conexión a {} fallido: {}'.format(
                        i, self._host, bte.message))
                else:
                    break
            else:
                raise TortoiseError(
                    "No se pudo establecer la conexión Bluetooth con {}".format(self._host))
            self._connected = True
        return self._connected

    def send(self, data):
        """lazy initialization. On 1st send"""
        if self._connected or self._connect():
            try:
                return self.bt_socket.send(data)
            except bt.BluetoothError as bte:
                raise TortoiseError(bte.message)

        raise TortoiseError('Error de conexión BT')

    def receive(self, buff=1024):
        if self._connected:
            return self.bt_socket.recv(buff)
        raise TortoiseError('Error de conexión BT')

    def disconnect(self):
        if self._connected:
            self.bt_socket.close()
            self._connected = False

    def __repr__(self):
        return str(self._host)


class Tortoise(object):
    """ Este objeto representa la Tortuga. Esto es un borrador.
    Necesita la ruta del archivo donde se encuentra la MAC
    del BT de la Tortuga."""

    def __init__(self, macfile):
        """ Inicia el objeto con la MAC extraida del archivo. Habra que hacer
        comprobaciones y puede que algun testeo u otras formas de definirlo"""
        mac = None
        try:
            with open(macfile, "r") as mf:
                mac = mf.read().strip()
        except:
            print("El archivo '{}' no existe.".format(macfile))
            mac = input("Introduce la MAC del BT de la Tortuga: ").strip()

        # tiene que ser una MAC valida
        if re.match("[0-9a-fA-F]{2}([-:])[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$", mac):
            self._bt = _TortoiseBT(mac)

        print(self, "-> CREATED")

    def start_drawing(self):
        """Empieza a dibujar"""
        print(self, "-> start_drawing")
        cmd = 'PD'
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def stop_drawing(self):
        """Deja de dibujar"""
        print(self, "-> stop_drawing")
        cmd = 'PU'
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def forward(self, units=10):
        """Avanza"""
        print(self, "-> forward", units)
        cmd = 'FD {}'.format(units)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def backward(self, units=10):
        """Retrocede"""
        print(self, "-> backward", units)
        cmd = 'BK {}'.format(units)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def turn_right(self, deg=90):
        """Gira en sentido horario, 90º por defecto"""
        print(self, "-> turn_right", deg)
        cmd = 'RT {}'.format(deg)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def turn_left(self, deg=90):
        """Gira en sentido antihorario, 90º por defecto"""
        print(self, "-> turn_left", deg)
        cmd = 'LT {}'.format(deg)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def read_sensor(self):
        """Lee el sensor de proximidad"""
        print(self, "-> read_sensor")
        cmd = 'OE'
        sensor = self._communicate(cmd, convert_func=lambda x: int(float(x)))
        if sensor:
            return sensor
        else:
            sys.exit(1)

    def _communicate(self, data, convert_func=lambda x: x):
        """Envia y recibe"""
        print(self, '{:<10} -> '.format(data), end='')
        try:
            r = self._bt.send(data + '\n')
            if data == str(r).strip():
                r = convert_func(self._bt.receive())
                print(r)
                return r
            else:
                print("Recibido:", r)
            
        except TortoiseError as te:
            print('ERROR')
            self._bt.disconnect()
            print(te.message, file=sys.stderr)
            sys.exit(1)
        # if OK, should not get here
        print('ERROR')
        return None  # return None to evaluate False on any command

    def __repr__(self):
        """Representacion de la tortuga para los print.
        Pretende ser una tortuga con la MAC en el caparazon xD"""
        return "}(" + str(self._bt) + "){o"
