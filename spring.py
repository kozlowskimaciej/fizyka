import pygame

import constants


class SpringAttachment:
    @property
    def attachment(self) -> pygame.Vector2:
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
        self.dumping = 2 * 100000

        self.force = 0
        self.last_dx = self.dx
        self.dx_change = 0

        self.rect.x = 45

    @property
    def dx(self) -> float:
        return self.attch1.attachment.y - self.attch2.attachment.y + self.max_length

    @property
    def is_max(self):
        return self.dx <= 0

    @property
    def is_min(self):
        return self.dx >= self.max_length - self.min_length

    def up(self, dt: float):
        self.rect.y = int((self.attch1.attachment.y + self.attch2.attachment.y) / 2)

        limited_dx = max(min(self.dx, self.max_length), 0)
        self.dx_change = limited_dx - self.last_dx
        self.last_dx = limited_dx

        dump = self.dx_change * dt * self.dumping

        self.force = self.k * limited_dx
        print(f"spring {self.force:10.1f}, dump {dump:10.1f}, dx: {self.dx:10.1f}")
        self.force += dump
