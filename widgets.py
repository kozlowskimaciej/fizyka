import pygame
from pygame_widgets.slider import Slider


class LabeledSlider:
    def __init__(self, surface, x, y, width, height, min_value, max_value, initial_value, on_change, name):
        super().__init__()
        self.surface = surface
        self.slider = Slider(
            surface,
            x=x,
            y=y + 20,
            width=width,
            height=height,
            min=min_value,
            max=max_value,
            step=1,
            initial=initial_value,
            handleColour=(255, 0, 0),
            barColour=(0, 255, 0),
            outlineColour=(0, 0, 0)
        )
        self.name = name
        self.font = pygame.font.SysFont('Arial', 24)
        self.x = x
        self.y = y
        self.current_value = initial_value
        self.on_change = on_change

    def draw(self):
        self.slider.draw()

        name_label = self.font.render(self.name, True, (0, 0, 0))
        name_rect = name_label.get_rect(
            center=(self.x + self.slider.getWidth() // 2,
                    self.y))
        self.surface.blit(name_label, name_rect)

        self.current_value = self.slider.getValue()
        current_label = self.font.render(f"{self.current_value}", True, (0, 0, 0))
        current_rect = current_label.get_rect(
            center=(self.x + self.slider.getWidth() // 2,
                    self.slider.getY() + self.slider.getHeight() + 15))
        self.surface.blit(current_label, current_rect)

        min_label = self.font.render(f"{self.slider.min}", True, (0, 0, 0))
        max_label = self.font.render(f"{self.slider.max}", True, (0, 0, 0))
        self.surface.blit(min_label,
                          (self.x - min_label.get_width() - 15,
                           self.y + self.slider.getHeight()))
        self.surface.blit(max_label,
                          (self.x + self.slider.getWidth() + 15,
                           self.y + self.slider.getHeight()))

    def update(self):
        self.on_change(self.current_value)

    def get_value(self):
        return self.current_value
