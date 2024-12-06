from abc import ABC, abstractmethod
import pygame

import constants


class SpringAttachment(ABC):
    @property
    @abstractmethod
    def spring_attachment(self) -> float:
        pass


class Spring(pygame.sprite.Sprite):
    def __init__(self, attch1: SpringAttachment, attch2: SpringAttachment):
        super().__init__()
        self.image = pygame.Surface([10, 150])
        self.image.fill(constants.WHITE)
        self.image.set_colorkey(constants.WHITE)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        pygame.draw.rect(self.image, constants.BLUE, rect=self.rect)

        self.attch1 = attch1
        self.attch2 = attch2

        self.k = 4500
        self.min_length = 50
        self.max_length = 200
        self.damping = 2 * 100000

        self.force = 0
        self.last_dx = self.dx
        self.dx_change = 0

        self.rect.x = 45

    @property
    def dx(self) -> float:
        return self.attch1.spring_attachment - self.attch2.spring_attachment + self.max_length

    @property
    def is_max(self):
        return self.dx <= 0

    @property
    def is_min(self):
        return self.dx >= self.max_length - self.min_length

    def update(self, dt):
        self.rect.y = int(
            (self.attch1.spring_attachment + self.attch2.spring_attachment - self.rect.h) / 2
        )

    def up(self, dt: float):
        tolerance = 10**-3
        assert 0 - tolerance <= self.dx <= self.max_length + tolerance, self.dx

        self.dx_change = self.dx - self.last_dx
        self.last_dx = self.dx

        damp = self.dx_change * dt * self.damping

        self.force = self.k * self.dx
        print(f"spring {self.force:10.1f}, damp {damp:10.1f}, dx: {self.dx:10.1f}")
        self.force += damp
