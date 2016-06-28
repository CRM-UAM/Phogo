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
    print("You can get it by typing the following command 'pip3 install pybluez' in your shell")
    sys.exit(1)

# shortcut
BluetoothError = bt.btcommon.BluetoothError

try:
    input = raw_input
except:
    pass

from time import sleep


class TortoiseError(Exception):
    pass


class _TortoiseBT(object):
    """Class that performs the BT communication between the
    computer and the Tortoise itself.
    """

    def __init__(self, host, port=1, connection_delay=2):
        self.bt_socket = None
        self._host = host
        self._port = port
        self._delay = connection_delay
        self._connected = False
        try:
            self._connect()
        except TortoiseError as te:
            print(te)
            sys.exit(1)

    def _connect(self):
        if not self._connected:
            print("Conectando con", self, end=' ')
            for i in range(3):  # we try to connect 3 times at most
                try:
                    print('...', end='')
                    self.bt_socket = bt.BluetoothSocket(bt.RFCOMM)
                    self.bt_socket.connect((self._host, self._port))
                except BluetoothError as bte:
                    pass
                else:
                    self.bt_socket.settimeout(5)
                    # apparently, it needs a timeout
                    # sleep(self._delay)
                    print(" OK")
                    break
            else:
                print(" ERROR")
                raise TortoiseError(
                    "No se pudo establecer la conexión Bluetooth con {}".format(self._host))
            self._connected = True
        return self._connected

    def send(self, data):
        """Sends `data` as a byte array."""
        if self._connected:
            try:
                return self.bt_socket.send(data.encode())
            except BluetoothError as bte:
                raise TortoiseError(bte)

        raise TortoiseError('Error de conexión BT: envío')

    def receive(self, buff=1024):
        """Receives whatever there is in the BT buffer and converts it to utf-8."""
        ret = ''
        if self._connected:
            try:
                #ret = self.bt_socket.recv(buff).decode("utf-8")
                while not ret.endswith('\n'):
                    ret += self.bt_socket.recv(buff).decode("utf-8")
                # return self.bt_socket.recv(buff).decode("utf-8")
                ret = ret.strip()
                # print(ret)
                return ret
            except:
                pass
        raise TortoiseError('Error de conexión BT: recepción')

    def disconnect(self):
        if self._connected:
            self.bt_socket.close()
            self._connected = False

    def __repr__(self):
        return str(self._host)


class Tortoise(object):
    """ Este objeto representa la Tortuga."""

    def __init__(self, mac):
        """Inicia el objeto con la MAC con la que se va a comunicar."""

        # tiene que ser una MAC valida
        if re.match(r'[0-9a-fA-F]{2}([-:])[0-9a-fA-F]{2}(\1[0-9a-fA-F]{2}){4}$', mac):
            self._bt = _TortoiseBT(mac)
            print(self, '->', self._bt.receive().strip().upper())
        else:
            raise TortoiseError("MAC is invalid")

    def start_drawing(self):
        """Empieza a dibujar"""
        #print(self, "-> start_drawing")
        cmd = 'PD'
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def stop_drawing(self):
        """Deja de dibujar"""
        #print(self, "-> stop_drawing")
        cmd = 'PU'
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def forward(self, units=10):
        """Avanza"""
        #print(self, "-> forward", units)
        cmd = 'FD {}'.format(units)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def backward(self, units=10):
        """Retrocede"""
        #print(self, "-> backward", units)
        cmd = 'BK {}'.format(units)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def turn_right(self, deg=90):
        """Gira en sentido horario, 90º por defecto"""
        #print(self, "-> turn_right", deg)
        cmd = 'RT {}'.format(deg)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def turn_left(self, deg=90):
        """Gira en sentido antihorario, 90º por defecto"""
        #print(self, "-> turn_left", deg)
        cmd = 'LT {}'.format(deg)
        if not self._communicate(cmd, convert_func=lambda x: str(x).strip().upper()) == 'OK':
            sys.exit(1)

    def read_sensor(self):
        """Lee el sensor de proximidad"""
        #print(self, "-> read_sensor")
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
            if len(data) + 1 == self._bt.send(data + '\n'):  # sending worked
                r = convert_func(self._bt.receive())
                print(r)
                return r
        except TortoiseError as te:
            print('ERROR')
            self._bt.disconnect()
            print(te, file=sys.stderr)
            sys.exit(1)
        # if OK, should not get here
        print('ERROR')
        return None  # return None to evaluate False on any command

    def __repr__(self):
        """Representacion de la tortuga para los print.
        Pretende ser una tortuga con la MAC en el caparazon xD"""
        return "}(" + str(self._bt) + "){o"
