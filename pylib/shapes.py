from crmphogo import *


def star(n_vertices=5, alternos=2, longitud=10):
    from fractions import gcd
    if 2 < 2 * alternos < n_vertices and gcd(n_vertices, alternos) == 1:
        angle = 180 - (180 * (n_vertices - 2 * alternos) // n_vertices)
        for i in range(n_vertices):
            pendown()
            forward(longitud)
            penup()
            right(angle)
    else:
        print('Parametros imposibles')


def koch_flake(numIter, longitud=10):
    def iteration(path):
        return path.replace("A", "AIADDAIA")

    def draw(path, longitud=30):
        pendown()
        for letter in path:
            if letter == "A":
                forward(longitud)
            elif letter == "D":
                right(60)
            elif letter == "I":
                left(60)

    initial_path = "ADDADDADD"  # Triángulo equilátero

    path = initial_path

    for i in range(numIter):
        path = iteration(path)

    draw(path, longitud)
