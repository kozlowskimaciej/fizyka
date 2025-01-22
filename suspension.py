from collections import deque
import time

import pygame

import constants
import matplotlib.pyplot as plt
from body import Body
import globals
from spring import Spring
from wheel import Wheel


class Suspension(pygame.sprite.Group):
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self._wheel = Wheel(radius=125, position=(410, 115))
        self._body = Body(position=(1, -175))
        self._spring = Spring(
            self._body,
            self._wheel,
            x_cord=self._wheel.x_cord + self._wheel.radius,
        )

        self.start_time = time.time()

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.fig.canvas.manager.set_window_title("Car")
        self.ax1.set_ylabel("Spring dx")
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Body y_cord")
        self.data_len = 100
        self.time_history = deque(maxlen=self.data_len)
        self.dx_history = deque(maxlen=self.data_len)
        self.body_y_cord_history = deque(maxlen=self.data_len)

        plt.ion()
        super().__init__([self._spring, self._body, self._wheel])

    def plot_update(self):
        current_time = time.time() - self.start_time

        self.time_history.append(current_time)
        self.dx_history.append(self._spring.dx)
        self.body_y_cord_history.append(constants.GROUND_LEVEL - self._body.y_cord)

        self.ax1.clear()
        self.ax2.clear()

        self.ax1.plot(self.time_history, self.dx_history)
        self.ax1.set_ylim(0, self._spring.max_length)
        self.ax1.set_ylabel("Spring x position offset")

        self.ax2.plot(self.time_history, self.body_y_cord_history)
        self.ax2.set_ylim(0, constants.WINDOW_SIZE[1] * 1.25)
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Body y position")

    def physics_update(self, dt: float):
        self._spring.physics_update(dt)
        self._apply_acceleration(
            self._wheel, globals.GRAVITY + self._spring.force / self._wheel.mass, dt
        )
        self._apply_acceleration(
            self._body,
            globals.GRAVITY - (self._spring.force + self._spring.damp) / self._body.mass,
            dt,
        )

        # Prevent falling below ground
        if self._wheel.y_cord > constants.GROUND_LEVEL:
            self._wheel.y_velocity = min(self._wheel.y_velocity, 0)
            self._wheel.y_cord = constants.GROUND_LEVEL

        self._wheel.collide(self.obstacles)

        # Prevent spring from stretching more that max_length
        if self._spring.is_max:
            self._wheel.y_velocity = min(self._wheel.y_velocity, self._body.y_velocity)
            self._wheel.spring_attachment = min(
                self._wheel.spring_attachment,
                self._body.spring_attachment + self._spring.max_length,
            )

        # Prevent body from falling below the wheel (with min_length gap)
        if self._spring.is_min and self._wheel.on_ground:
            self._body.spring_attachment = min(
                self._body.spring_attachment,
                self._wheel.spring_attachment - self._spring.min_length,
            )
            self._body.y_velocity = min(self._body.y_velocity, self._wheel.y_velocity)

    @staticmethod
    def _apply_acceleration(obj, acc, dt):
        obj.y_velocity += acc * dt
        obj.y_cord += obj.y_velocity * dt
