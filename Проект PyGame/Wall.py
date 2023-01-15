from LoadImage import load_image
import pygame as pg
import random


class Wall():
    def __init__(self):
        width, height = 800, 600
        self.angle = random.randint(0, 1)
        if self.angle == 0:
            self.picture = load_image("ladder_v.png")
        else:
            self.picture = load_image("ladder_h.png")

        a = [random.randint(0, width // 2 - self.picture.get_rect().width),
             random.randint(width // 2 + self.picture.get_rect().width, width - self.picture.get_rect().width)]
        b = [random.randint(0, height // 2 - self.picture.get_rect().height),
             random.randint(height // 2 + self.picture.get_rect().height, height - self.picture.get_rect().height)]

        self.rect = pg.Rect((a[random.randint(0, 1)], b[random.randint(0, 1)],
                             self.picture.get_rect().width,
                             self.picture.get_rect().height))
