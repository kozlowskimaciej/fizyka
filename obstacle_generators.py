from random import randint

import pygame

import constants
from obstacles import Bump


INIT_POSITION = (constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]-50)


def generate_obstacle() -> Bump:
    return Bump(INIT_POSITION, 150)


class TrackGenerator:
    gen_param: int = 100

    def generate(self) -> Bump | None:
        pass


class RandomGenerator(TrackGenerator):
    def generate(self) -> Bump | None:
        if randint(0, self.gen_param) < 5:
            return generate_obstacle()
        return None


class RegularGenerator(TrackGenerator):
    def __init__(self, interval: int = 100):
        self.next_obstacle_time = 0
        self.gen_param = interval

    def generate(self) -> Bump | None:
        if pygame.time.get_ticks() > self.next_obstacle_time:
            self.next_obstacle_time += self.gen_param
            return generate_obstacle()
        return None
