from random import randint
import pygame.rect
import pygame
from pygame.locals import *

from body import Body
from spring import Spring
from wheel import Wheel
from obstacles import Bump


import constants

clock = pygame.time.Clock()


class Supsension(pygame.sprite.Group):
    def __init__(self):
        self._wheel = Wheel(radius=50, position=(100, 290))
        self._body = Body()
        self._spring = Spring(self._body, self._wheel)
        self._body.spring = self._spring
        self._wheel.spring = self._spring
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
        self._suspension = Supsension()
        self._obstacles = pygame.sprite.Group()
        self._sprites = pygame.sprite.Group(
            self._suspension,
            self._obstacles)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, dt):
        self._sprites.update(dt=dt)
        self._suspension._wheel.collide(self._obstacles)

        if randint(0, 100) == 0:
            bump = Bump((640, 350), 75)
            self._sprites.add(bump)
            self._obstacles.add(bump)

    def on_render(self):
        self._display_surf.fill(constants.WHITE)
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
