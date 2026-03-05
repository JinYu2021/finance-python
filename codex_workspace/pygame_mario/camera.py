import pygame

from settings import WIDTH


class Camera:
    def __init__(self, world_width: int) -> None:
        self.world_width = world_width
        self.x = 0.0

    def update(self, target_world_x: float) -> None:
        desired_x = target_world_x - WIDTH / 2
        max_x = max(0, self.world_width - WIDTH)
        self.x = max(0.0, min(desired_x, float(max_x)))

    def world_to_screen(self, world_x: float, world_y: float) -> tuple[int, int]:
        return int(world_x - self.x), int(world_y)

    def world_to_screen_rect(self, world_rect: pygame.Rect) -> pygame.Rect:
        sx, sy = self.world_to_screen(world_rect.x, world_rect.y)
        return pygame.Rect(sx, sy, world_rect.width, world_rect.height)
