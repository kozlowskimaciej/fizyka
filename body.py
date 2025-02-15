import pygame

from spring import SpringAttachment


class Body(pygame.sprite.Sprite, SpringAttachment):
    def __init__(self, position: tuple[int, int]):
        super().__init__()

        self.x_cord: float = position[0]
        self.y_cord: float = position[1]
        self.y_velocity: float = 0

        self.image = pygame.image.load("img/car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (850, 450))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord

        self.spring_offset = self.rect.h - 125
        self.mass = 400

    def update(self, dt):
        self.rect.y = int(self.y_cord)
