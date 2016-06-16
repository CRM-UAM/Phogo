# -*- coding: utf-8 -*-
# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain
from __future__ import print_function  # python2 compatibility

import sys
try:
    import bluetooth as bt
except ImportError:
    print("PyBluez must be installed.")
    #sys.exit(1)
import os

class TortoiseBTClient(object):
    """docstring for TortoiseBT"""
    def __init__(self, host, port):
        self.bt_socket = bt.BluetoothSocket( bt.RFCOMM )
        self._host = host
        self._port = port

        self._connected = False

    def connect(self):
        if not self._connected:
            for i in range(3):
                self.bt_socket.connect((self._host, self._port))
            else:
                print("No se pudo establecer la conexión Bluetooth.")
                sys.exit(1)
            self._connected = True
        return self._connected

    


class Tortoise(object):
    """ Este objeto representa la Tortuga. Esto es un borrador.
    Necesita la ruta del archivo donde se encuentra la MAC
    del BT de la Tortuga."""

    def __init__(self, macfile):
        """ Inicia el objeto con la MAC extraida del archivo. Habra que hacer
        comprobaciones y puede que algun testeo u otras formas de definirlo"""
        try:
            with open(macfile, "r") as mf:
                self.mac = mf.read().rstrip()
        except:
            print("El archivo '{}' no existe.".format(macfile))
            self.mac = input("Introduce la MAC del BT de la Tortuga: ")

        print(self, "-> CREATED")

    def start_drawing(self):
        """Empieza a dibujar"""
        print(self, "-> start_drawing")

    def stop_drawing(self):
        """Deja de dibujar"""
        print(self, "-> stop_drawing")

    def forward(self, units=10):
        """Avanza"""
        print(self, "-> forward", units)

    def backward(self, units=10):
        """Retrocede"""
        print(self, "-> backward", units)

    def turn_right(self, deg=90):
        """Gira 90º en sentido horario"""
        print(self, "-> turn_right", deg)

    def turn_left(self, deg=-90):
        """Gira 90º en sentido antihorario"""
        print(self, "-> turn_left", deg)
        
    def _comm(self, data):
        """La idea es que esta funcion envíe la info y reciba el OK"""
        pass

    def __repr__(self):
        """Representacion de la torutga para los print.
        Pretende ser una tortuga con la MAC en el caparazon xD"""
        return "}(" + self.mac + "){o"

    def run_program(self):
        print(self, "-> run_program")