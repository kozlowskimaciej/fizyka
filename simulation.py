from dataclasses import dataclass

import pygame.rect
import pygame
from pygame.locals import *


RED = (255, 0, 0)
BLUE = (50, 255, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 60

clock = pygame.time.Clock()


@dataclass
class Point:
    x: float
    y: float


class SpringAttachment:
    @property
    def attachment(self) -> Point:
        pass


class Spring(pygame.sprite.Sprite):
    def __init__(self, attch1: SpringAttachment, attch2: SpringAttachment):
        super().__init__()
        self.image = pygame.Surface([10, 100])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect: pygame.rect.Rect = self.image.get_rect()

        self.attch1 = attch1
        self.attch2 = attch2

        self.max_length = 50

        pygame.draw.rect(self.image, BLUE, rect=self.rect)

    def update(self, dt: float):
        self.rect.y = int(
            (self.attch1.attachment.y + self.attch2.attachment.y) / 2
        )
        self.rect.h = 1
        pygame.draw.rect(self.image, BLUE, rect=self.rect)
        # self.rect.height = abs(
        #     self.attch1.attachment.y - self.attch2.attachment.y
        # )

    @property
    def force(self) -> float:
        dx = max(
            min(self.attch2.attachment.y - self.attch1.attachment.y + 200, 50),
            0,
        )
        f = 1.5 * dx
        return f


class Wheel(pygame.sprite.Sprite):
    def __init__(self, radius: int, position: tuple[int, int]):
        super().__init__()
        self.y_velocity: float = 0
        self.radius = radius
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x_cord: float = float(position[0])
        self.y_cord: float = float(position[1])
        pygame.draw.circle(
            self.image,
            BLACK,
            [self.x_cord - radius, self.y_cord - radius],
            self.radius,
            width=0,
        )

    def update(self, dt: float):
        self.y_velocity += GRAVITY * dt
        self.y_cord += self.y_velocity * dt

        if self.y_cord > 300:
            self.y_velocity = 0
            self.y_cord = 300
        self.rect.y = int(self.y_cord)

    @property
    def attachment(self) -> Point:
        return Point(self.x_cord, self.y_cord)

    @property
    def on_ground(self) -> bool:
        return self.y_cord > 299


class Body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.spring: None | Spring = None

        self.x_cord: float = float(200)
        self.y_cord: float = float(200)

        self.y_velocity: float = 0

        self.mass = 1000

        pygame.draw.rect(self.image, RED, rect=self.rect)
        self.rect.y = self.y_cord

    def update(self, dt: float):
        force = GRAVITY - self.spring.force
        self.y_velocity += force * dt
        self.y_cord += self.y_velocity * dt
        self.rect.y = int(self.y_cord)

    @property
    def attachment(self) -> Point:
        return Point(self.x_cord, self.y_cord)


class Supsension(pygame.sprite.Group):
    def __init__(self):
        self._wheel = Wheel(radius=50, position=(100, 100))
        self._body = Body()
        self._spring = Spring(self._wheel, self._body)
        self._body.spring = self._spring
        super().__init__([self._wheel, self._body, self._spring])


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._sprites = Supsension()
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, dt):
        self._sprites.update(dt=dt)

    def on_render(self):
        self._display_surf.fill(WHITE)
        self._sprites.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(dt=dt)
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()
