from math import sqrt
import pygame

import constants
from spring import Spring
from utils import change_abs_value


class Body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([400, 50])
        self.image.fill(constants.WHITE)
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, constants.RED, rect=self.rect)

        self.x_cord: float = float(25)
        self.y_cord: float = float(150)
        self.rect.y = self.y_cord
        self.rect.x = self.x_cord

        self.y_velocity: float = 0

        self.mass = 400

        self.spring: None | Spring = None

    def update(self, dt: float):
        acceleration = constants.GRAVITY - self.spring.force / self.mass
        self.y_velocity += acceleration * dt

        dumping = abs(self.spring.dx_change * dt) / self.mass * 10000
        self.y_velocity = change_abs_value(self.y_velocity, -dumping)

        # print(f"force {self.spring.force} dumping {dumping}")

        self.y_cord += self.y_velocity * dt

        # Prevent falling below the wheel (with min_length gap)
        if self.spring.is_min:
            self.y_cord = self.spring.other_attachment(self).attachment.y - self.spring.min_length
            self.y_velocity = max(self.y_velocity, 0)

        self.rect.y = int(self.y_cord)

    @property
    def attachment(self) -> pygame.Vector2:
        return pygame.Vector2(self.x_cord, self.y_cord)
