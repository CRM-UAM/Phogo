from crmphogo import *


def star(n_vertices=5, alternos=2, longitud=10):
    from fractions import gcd
    if 2 < 2 * alternos < n_vertices and gcd(n_vertices, alternos) == 1:
        angle = 180 - (180 * (n_vertices - 2 * alternos) // n_vertices)
        for i in range(n_vertices):
            pen_down()
            forward(longitud)
            pen_up()
            right(angle)
    else:
        print('Parametros imposibles')


def koch_flake(numIter, longitud=10):
    def iteration(path):
        return path.replace("A", "AIADDAIA")

    def draw(path, longitud=30):
        pen_down()
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


def circle(radius=20, angle=5, cw=True):
    from math import pi, sin, radians, degrees

    pen_down()

    angle = radians(angle)
    l = int(radius * 2 * sin(angle / 2) + .5)
    turn = right if cw else left

    if 5 > angle > 10:
        print("El angulo tiene que estar entre 5 y 10.")
        return
    elif l < 1:
        print("Radio demasiado pequeño para ese angulo.")
        return

    #angle = 180 - 2 * angle
    acc_angle = 0

    pen_down()
    while acc_angle < 2*pi:
        forward(l)
        turn(degrees(angle))
        acc_angle += angle

    pen_up()