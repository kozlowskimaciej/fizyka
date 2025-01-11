import pygame

import globals


class Body(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()

        self.x_cord: float = position[0]
        self.y_cord: float = position[1]
        self.y_velocity: float = 0

        self.image = pygame.image.load('img/car.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (800, 450))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord

        self.spring_attachment_offset = self.rect.h
        self.mass = 400

    def update(self, dt):
        self.rect.y = int(self.y_cord)

    @property
    def spring_attachment(self) -> float:
        return self.y_cord + self.spring_attachment_offset

    @spring_attachment.setter
    def spring_attachment(self, val: float) -> float:
        self.y_cord = val - self.spring_attachment_offset
