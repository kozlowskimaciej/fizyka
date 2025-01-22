import pygame
import globals


class SpringAttachment:
    @property
    def spring_attachment(self) -> float:
        return self.y_cord + self.spring_offset

    @spring_attachment.setter
    def spring_attachment(self, value: float) -> None:
        self.y_cord = value - self.spring_offset


class Spring(pygame.sprite.Sprite):
    orig_image = pygame.image.load("img/spring.jpg")

    def __init__(self, attch1: SpringAttachment, attch2: SpringAttachment, x_cord: int):
        super().__init__()

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.x_cord = x_cord

        self.attch1 = attch1
        self.attch2 = attch2

        self.min_length = 5
        self.max_length = 200

        self.force = 0
        self.last_dx = self.dx
        self.dx_change = 0


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
        self.image = pygame.transform.scale(self.orig_image, (80, (self.max_length - self.dx)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_cord - self.rect.w / 2
        self.rect.y = (
            self.attch1.spring_attachment + self.attch2.spring_attachment - self.rect.h
        ) / 2

    def physics_update(self, dt: float):
        tolerance = 10**-3
        assert 0 - tolerance <= self.dx <= self.max_length + tolerance, self.dx

        self.dx_change = self.dx - self.last_dx
        self.last_dx = self.dx

        self.damp = self.dx_change * dt * globals.DAMPING

        self.force = globals.SPRINGINESS * self.dx
        # print(f"spring {self.force:10.1f}, damp {self.damp:10.1f}, dx: {self.dx:10.1f}")
