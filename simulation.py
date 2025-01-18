import time

from matplotlib import pyplot as plt
import pygame
import pygame_widgets

import globals
from obstacle_generators import RandomGenerator, RegularGenerator, TrackGenerator
from suspension import Supsension
from widgets import LabeledSlider, UpdatableDropdown

clock = pygame.time.Clock()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = globals.WINDOW_SIZE
        self.gravity_slider = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._obstacles = pygame.sprite.Group()
        self._suspension = Supsension(self._obstacles)
        self._sprites = pygame.sprite.Group(self._suspension, self._obstacles)
        self._running = True
        self.track_generator: TrackGenerator = RegularGenerator()
        self.slider_width = 150
        self.gui_x_cord = globals.WINDOW_SIZE[0] - self.slider_width - 130
        self._gui = [
            LabeledSlider(
                self._display_surf,
                x=self.gui_x_cord,
                y=50,
                width=self.slider_width,
                height=10,
                min_value=0,
                max_value=600,
                initial_value=globals.GRAVITY,
                on_change=lambda val: setattr(globals, "GRAVITY", val),
                name="Gravity",
            ),
            LabeledSlider(
                self._display_surf,
                x=self.gui_x_cord,
                y=150,
                width=self.slider_width,
                height=10,
                min_value=0,
                max_value=600000,
                initial_value=globals.DAMPING,
                on_change=lambda val: setattr(globals, "DAMPING", val),
                name="Damping",
            ),
            LabeledSlider(
                self._display_surf,
                x=self.gui_x_cord,
                y=250,
                width=self.slider_width,
                height=10,
                min_value=0,
                max_value=6000,
                initial_value=globals.SPRINGINESS,
                on_change=lambda val: setattr(globals, "SPRINGINESS", val),
                name="Springiness",
            ),
            LabeledSlider(
                self._display_surf,
                x=self.gui_x_cord,
                y=350,
                width=self.slider_width,
                height=10,
                min_value=20,
                max_value=20000,
                initial_value=20000,
                on_change=lambda val: setattr(app.track_generator, "gen_param", val),
                name="Generator param",
            ),
            UpdatableDropdown(
                on_change=self._change_track_generator,
                win=self._display_surf,
                x=650,
                y=150,
                width=150,
                height=50,
                name="Regular",
                choices=[
                    "Random",
                    "None",
                    "Regular",
                ],
                borderRadius=3,
            ),
        ]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, dt):
        self._sprites.update(dt=dt)
        self._suspension.up(dt)
        for it in self._gui:
            it.update()

        if bump := self.track_generator.generate():
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
        last_frame_t = time.time()
        while self._running:
            if (sleep_t := time.time() - last_frame_t) and sleep_t < 0.05:
                time.sleep(0.05 - sleep_t)
            last_frame_t = time.time()
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            pygame_widgets.update(events)
            self.on_loop(dt=0.04)
            self.on_render()
            plt.draw()
            plt.pause(0.01)
        self.on_cleanup()

    def _change_track_generator(self, value):
        if value == "Random":
            self.track_generator = RandomGenerator()
        elif value == "Regular":
            self.track_generator = RegularGenerator()
        elif value == "None":
            self.track_generator = TrackGenerator()
        else:
            raise ValueError(f"Invalid value: {value}")


if __name__ == "__main__":
    app = App()
    app.on_execute()
