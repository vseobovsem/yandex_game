import os
import pygame as pg


def load_image(name, colorkey=None):
    fullname = os.path.join('Data', name)
    image = pg.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__load_image__':
    load_image()
