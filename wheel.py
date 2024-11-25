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

        self.spring: None | Spring = None

        pygame.draw.circle(
            self.image,
            constants.BLACK,
            [radius, radius],
            self.radius,
            width=0,
        )

    def update(self, dt: float):
        self.y_velocity += constants.GRAVITY * dt
        self.y_cord += self.y_velocity * dt

        # Prevent spring from stretching more that max_length
        if self.spring.is_max:
            self.y_velocity = self.spring.other_attachment(self).y_velocity
            self.y_cord = (
                self.spring.other_attachment(self).attachment.y
                + self.spring.max_length
            )
        # Prevent falling below ground
        elif self.y_cord > 300:
            self.y_velocity = max(self.y_velocity, 0)
            self.y_cord = 300
        self.rect.y = int(self.y_cord)

    @property
    def attachment(self) -> pygame.Vector2:
        return pygame.Vector2(self.x_cord, self.y_cord)

    @property
    def on_ground(self) -> bool:
        return self.y_cord > 299
