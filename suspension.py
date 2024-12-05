import pygame
from body import Body
import constants
from spring import Spring
from wheel import Wheel


class Supsension(pygame.sprite.Group):
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self._wheel = Wheel(radius=50, position=(100, 240))
        self._body = Body()
        self._spring = Spring(self._body, self._wheel)
        self._body.spring = self._spring
        self._wheel.spring = self._spring
        super().__init__([self._wheel, self._body, self._spring])

    ground_level = 300

    def up(self, dt: float):
        self._spring.up(dt)
        self._apply_acceleration(
            self._wheel, constants.GRAVITY + self._spring.force / self._wheel.mass, dt
        )
        self._apply_acceleration(
            self._body, constants.GRAVITY - self._spring.force / self._body.mass, dt
        )

        # Prevent falling below ground
        if self._wheel.y_cord > self.ground_level:
            self._wheel.y_velocity = min(self._wheel.y_velocity, 0)
            self._wheel.y_cord = self.ground_level

        self._wheel.collide(self.obstacles)

        # Prevent spring from stretching more that max_length
        if self._spring.is_max:
            self._wheel.y_velocity = min(self._wheel.y_velocity, self._body.y_velocity)
            self._wheel.y_cord = min(
                self._wheel.y_cord, self._body.y_cord + self._spring.max_length
            )

        # Prevent body from falling below the wheel (with min_length gap)
        if self._spring.is_min and self._wheel.on_ground:
            self._body.y_cord = min(self._body.y_cord, self._wheel.y_cord - self._spring.min_length)
            self._body.y_velocity = min(self._body.y_velocity, self._wheel.y_velocity)

    @staticmethod
    def _apply_acceleration(obj, acc, dt):
        obj.y_velocity += acc * dt
        obj.y_cord += obj.y_velocity * dt
