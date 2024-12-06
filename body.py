import pygame

import constants


class Body(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()

        self.x_cord: float = position[0]
        self.y_cord: float = position[1]
        self.y_velocity: float = 0

        self.image = pygame.Surface([400, 50])
        self.image.fill(constants.WHITE)
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x_cord
        pygame.draw.rect(self.image, constants.RED, rect=self.rect)

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
