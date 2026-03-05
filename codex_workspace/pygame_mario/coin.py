import pygame

from settings import COIN_COLOR, COIN_SIZE


class Coin:
    def __init__(self, center_x: float, center_y: float) -> None:
        size = COIN_SIZE
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (int(center_x), int(center_y))
        self.collected = False

    def collect(self) -> None:
        self.collected = True

    def draw(self, surface: pygame.Surface, camera) -> None:
        if self.collected:
            return
        screen_rect = camera.world_to_screen_rect(self.rect)
        pygame.draw.ellipse(surface, COIN_COLOR, screen_rect)
