from random import randint

import pygame
import pygame_widgets

from suspension import Supsension
from obstacles import Bump
from custom_slider import CustomSlider

import globals


clock = pygame.time.Clock()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.gravity_slider = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._obstacles = pygame.sprite.Group()
        self._suspension = Supsension(self._obstacles)
        self._sprites = pygame.sprite.Group(self._suspension, self._obstacles)
        self._running = True
        self._gui = [
            CustomSlider(
                self._display_surf,
                x=50,
                y=50,
                width=150,
                height=10,
                min_value=0,
                max_value=600,
                initial_value=globals.GRAVITY,
                on_change=lambda val: setattr(globals, 'GRAVITY', val),
                name="Gravity"
            ),
            CustomSlider(
                self._display_surf,
                x=300,
                y=50,
                width=150,
                height=10,
                min_value=0,
                max_value=60000000,
                initial_value=globals.DAMPING,
                on_change=lambda val: setattr(globals, 'DAMPING', val),
                name="Damping"
            )]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, dt):
        self._sprites.update(dt=dt)
        self._suspension.up(dt)
        for it in self._gui:
            it.update()

        if randint(0, 100) < 1:
            bump = Bump((640, 350), 75)
            self._sprites.add(bump)
            self._obstacles.add(bump)

    def on_render(self):
        self._display_surf.fill(globals.WHITE)
        self._sprites.draw(self._display_surf)
        for it in self._gui:
            it.draw()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            dt = clock.tick(60) / 1000
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            pygame_widgets.update(events)
            self.on_loop(dt=dt)
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()
