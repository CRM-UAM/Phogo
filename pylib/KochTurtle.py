# -*- coding: utf-8 -*-
import turtle

# A -> Avanzar
# I -> 60º izquierda
# D -> 60º derecha

def iteracion_Koch(ruta):
	return ruta.replace("A", "AIADDAIA")

def pintar(ruta, longitud = 30):
	for letra in ruta:
		if letra == "A":
			turtle.forward(longitud)
		elif letra == "D":
			turtle.right(60)
		elif letra == "I":
			turtle.left(60)

def copo_Koch(numIter, longitud = 30):
	ruta_inicio = "ADDADDADD" # Triángulo equilátero
	
	ruta = ruta_inicio
	
	for i in range(numIter):
		ruta = iteracion_Koch(ruta)
	
	pintar(ruta, longitud)

		
