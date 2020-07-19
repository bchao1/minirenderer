import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (186, 218, 219)

def rand_color():
    return (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

def color_grad(color, intensity):
    return tuple(int(intensity * c) for c in color)