import pygame
from pygame.locals import *


RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Wheel(pygame.sprite.Sprite):
    def __init__(self, radius: int, position: tuple[int, int]):
        super().__init__()
        self.x_cord, self.y_cord = position
        self.radius = radius
        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(
            self.image,
            RED,
            [self.x_cord-radius, self.y_cord-radius],
            self.radius,
            width = 0)

        self.rect = self.image.get_rect()
        self.radius = 5

    def update(self):
        self.y_cord += 1
        if self.rect.centery:
            self.rect.y = 0
        self.rect.move_ip(0, 1)



class Supsension(pygame.sprite.Group):
    def __init__(self):
        self._wheel = Wheel(radius=50, position=(100, 100))
        # self._shock_absorber =
        # self._spring =
        # self._body =
        super().__init__([self._wheel])



class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._sprites = Supsension()
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self._sprites.update()

    def on_render(self):
        self._display_surf.fill(WHITE)
        self._sprites.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__" :
    app = App()
    app.on_execute()
