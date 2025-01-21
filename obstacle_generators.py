from random import randint

import pygame

import constants
import globals
from obstacles import Bump


INIT_POSITION = (constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]-50)


def generate_obstacle() -> Bump:
    return Bump(INIT_POSITION, 150)


class TrackGenerator:
    def generate(self) -> Bump | None:
        pass


class RandomGenerator(TrackGenerator):
    def generate(self) -> Bump | None:
        if randint(0, globals.GENERATOR_PARAM) < 5:
            return generate_obstacle()
        return None


class RegularGenerator(TrackGenerator):
    def __init__(self):
        self.last_obstacle_time = 0

    def generate(self) -> Bump | None:
        if pygame.time.get_ticks() > self.last_obstacle_time + globals.GENERATOR_PARAM:
            self.last_obstacle_time += globals.GENERATOR_PARAM
            return generate_obstacle()
        return None
