from typing import Iterable
import pygame

import constants
from spring import Spring


class Wheel(pygame.sprite.Sprite):
    def __init__(self, radius: int, position: tuple[int, int]):
        super().__init__()
        self.y_velocity: float = 0
        self.radius = radius
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(constants.WHITE)
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()

        self.x_cord: float = float(position[0])
        self.y_cord: float = float(position[1])
        self.mass = 5

        self.collision = True

        self.spring: None | Spring = None

        pygame.draw.circle(
            self.image,
            constants.BLACK,
            [radius, radius],
            self.radius,
            width=0,
        )

    def update(self, dt):
        self.rect.y = int(self.y_cord)

    def collide(self, others: Iterable[pygame.sprite.Sprite]) -> bool:
        y_diff = 0
        for other in others:
            while pygame.sprite.collide_mask(self, other):
                self.rect.y -= 1
                y_diff += 1

        self.collision = bool(y_diff)

        if self.collision:
            if self.y_velocity > 0:
                self.y_velocity = 0
            self.y_velocity = 0  # -y_diff * 40
            self.y_cord -= y_diff

    @property
    def attachment(self) -> pygame.Vector2:
        return pygame.Vector2(self.x_cord, self.y_cord)

    @property
    def on_ground(self) -> bool:
        return self.collision or self.y_cord >= 300
