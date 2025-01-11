from abc import ABC, abstractmethod
import pygame
import matplotlib.pyplot as plt
import time

import globals


class SpringAttachment(ABC):
    @property
    @abstractmethod
    def spring_attachment(self) -> float:
        pass


class Spring(pygame.sprite.Sprite):
    def __init__(self, attch1: SpringAttachment, attch2: SpringAttachment):
        super().__init__()
        self.image = pygame.Surface([10, 150])
        self.image.fill(globals.WHITE)
        self.image.set_colorkey(globals.WHITE)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        pygame.draw.rect(self.image, globals.BLUE, rect=self.rect)

        self.attch1 = attch1
        self.attch2 = attch2

        self.k = 4500
        self.min_length = 50
        self.max_length = 200

        self.force = 0
        self.last_dx = self.dx
        self.dx_change = 0

        self.rect.x = 45

        self.start_time = time.time()
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.fig.canvas.manager.set_window_title('Car')
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Spring dx')
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Body y_cord')
        self.x_data = []
        self.y_data = []
        self.y_cord_data = []

        plt.ion()


    @property
    def dx(self) -> float:
        return self.attch1.spring_attachment - self.attch2.spring_attachment + self.max_length

    @property
    def is_max(self):
        return self.dx <= 0

    @property
    def is_min(self):
        return self.dx >= self.max_length - self.min_length

    def update(self, dt):
        self.rect.y = int(
            (self.attch1.spring_attachment + self.attch2.spring_attachment - self.rect.h) / 2
        )

        current_time = time.time() - self.start_time
        self.x_data.append(current_time)
        self.y_data.append(self.dx)

        self.y_cord_data.append(self.attch1.y_cord)

        if len(self.x_data) > 1:
            self.ax1.set_xlim(max(0, max(self.x_data) - 30), max(self.x_data))
            self.ax2.set_xlim(max(0, max(self.x_data) - 30), max(self.x_data))
        else:
            self.ax1.set_xlim(0, 30)
            self.ax2.set_xlim(0, 30)

        self.ax1.clear()
        self.ax1.plot(self.x_data, self.y_data)
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Spring x position offset')

        self.ax2.clear()
        self.ax2.plot(self.x_data, self.y_cord_data)
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Body y position')

    def up(self, dt: float):
        tolerance = 10**-3
        assert 0 - tolerance <= self.dx <= self.max_length + tolerance, self.dx

        self.dx_change = self.dx - self.last_dx
        self.last_dx = self.dx

        self.damp = self.dx_change * dt * globals.DAMPING

        self.force = self.k * self.dx
        # print(f"spring {self.force:10.1f}, damp {self.damp:10.1f}, dx: {self.dx:10.1f}")
