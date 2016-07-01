from crmphogo import *

def star(n_vertices=5, alternos=2, longitud=10):
    from fractions import gcd
    if 2 < 2 * alternos < n_vertices and gcd(n_vertices, alternos) == 1:
        angle = 180 - (180 * (n_vertices - 2 * alternos) // n_vertices)
        for i in range(n_vertices):
            EmpezarADibujar()
            Avanzar(longitud)
            DejarDeDibujar()
            GirarDerecha(angle)
    else:
        print('Parametros imposibles')