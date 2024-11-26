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
        self.force = 0
        self.is_max = False
        self.is_min = False

        self.last_dx = 0
        self.dx_change = 0

        self.rect.x = 45

    def update(self, dt: float):
        self.rect.y = int((self.attch1.attachment.y + self.attch2.attachment.y) / 2)

        dx = self.attch1.attachment.y - self.attch2.attachment.y + self.max_length

        limited_dx = max(min(dx, self.max_length), 0)
        self.dx_change = limited_dx - self.last_dx
        self.last_dx = limited_dx
        self.force = self.k * limited_dx

        self.is_max = dx < 0
        self.is_min = dx > self.max_length - self.min_length

        # print( f"dx {limited_dx:.3f} force {self.force:.3f} max {self.is_max} min {self.is_min}")

    def other_attachment(self, obj):
        if obj == self.attch1:
            return self.attch2
        if obj == self.attch2:
            return self.attch1
