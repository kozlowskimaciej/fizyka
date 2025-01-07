from random import randint
from obstacles import Bump
import pygame

INIT_POSITION = (640, 350)


def generate_obstacle() -> Bump:
    return Bump(INIT_POSITION, 75)


class TrackGenerator:
    def generate(self) -> Bump | None:
        pass


class RandomGenerator(TrackGenerator):
    def generate(self) -> Bump | None:
        if randint(0, 100) < 1:
            return generate_obstacle()
        return None


class RegularGenerator(TrackGenerator):
    def __init__(self, interval: int):
        self.next_obstacle_time = 0
        self.interval = interval

    def generate(self) -> Bump | None:
        if pygame.time.get_ticks() > self.next_obstacle_time:
            self.next_obstacle_time += self.interval
            return generate_obstacle()
        return None
