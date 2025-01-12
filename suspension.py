import pygame
from body import Body
import globals
from spring import Spring
from wheel import Wheel


class Supsension(pygame.sprite.Group):
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self._wheel = Wheel(radius=125, position=(410, 115))
        self._body = Body(position=(1, -175))
        self._spring = Spring(
            self._body,
            self._wheel,
            x_cord=self._wheel.x_cord + self._wheel.radius,
        )
        super().__init__([self._spring, self._body, self._wheel])

    ground_level = globals.WINDOW_SIZE[1] - 250

    def up(self, dt: float):
        self._spring.up(dt)
        self._apply_acceleration(
            self._wheel, globals.GRAVITY + self._spring.force / self._wheel.mass, dt
        )
        self._apply_acceleration(
            self._body,
            globals.GRAVITY - (self._spring.force + self._spring.damp) / self._body.mass,
            dt,
        )

        # Prevent falling below ground
        if self._wheel.y_cord > self.ground_level:
            self._wheel.y_velocity = min(self._wheel.y_velocity, 0)
            self._wheel.y_cord = self.ground_level

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
                self._body.spring_attachment, self._wheel.y_cord - self._spring.min_length
            )
            self._body.y_velocity = min(self._body.y_velocity, self._wheel.y_velocity)

    @staticmethod
    def _apply_acceleration(obj, acc, dt):
        obj.y_velocity += acc * dt
        obj.y_cord += obj.y_velocity * dt
