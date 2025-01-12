from typing import Iterable
import pygame


class Wheel(pygame.sprite.Sprite):
    def __init__(self, radius: int, position: tuple[int, int]):
        super().__init__()

        self.radius = radius
        self.x_cord: float = float(position[0])
        self.y_cord: float = float(position[1])
        self.y_velocity: float = 0
        self.mass = 5

        self.image = pygame.image.load("img/wheel.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (2 * radius, 2 * radius))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_cord

        self.collision = False
        self.angle = 0

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
            self.y_velocity = min(self.y_velocity, 0)  # TODO: Set it to -sin(ground_angle)
            self.y_cord -= y_diff

    @property
    def spring_attachment(self) -> float:
        return self.y_cord + self.radius

    @spring_attachment.setter
    def spring_attachment(self, value) -> None:
        self.y_cord = value - self.radius

    @property
    def on_ground(self) -> bool:
        return self.collision or self.y_cord >= 300
