import pygame


class Bump(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], radius: int):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self, dt: float):
        self.rect.x -= dt * 400
        if self.rect.right < 0:
            self.kill()
