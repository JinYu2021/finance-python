import pygame

from settings import (
    ENEMY_COLOR,
    ENEMY_GRAVITY,
    ENEMY_HEIGHT,
    ENEMY_MOVE_SPEED,
    ENEMY_WIDTH,
)


class Enemy:
    def __init__(self, start_x: float, start_y: float) -> None:
        self.rect = pygame.Rect(int(start_x), int(start_y), ENEMY_WIDTH, ENEMY_HEIGHT)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vy = 0.0
        self.direction = 1
        self.alive = True
        self.on_ground = False

    def kill(self) -> None:
        self.alive = False

    def update(
        self,
        dt: float,
        solid_tiles: list[pygame.Rect],
        world_width: int,
        world_height: int,
    ) -> None:
        if not self.alive:
            return

        vx = self.direction * ENEMY_MOVE_SPEED
        self.x += vx * dt
        self.rect.x = int(self.x)

        hit_wall = False
        for tile in solid_tiles:
            if not self.rect.colliderect(tile):
                continue
            hit_wall = True
            if vx > 0:
                self.rect.right = tile.left
            else:
                self.rect.left = tile.right
            self.x = float(self.rect.x)

        if self.rect.left < 0:
            self.rect.left = 0
            self.x = float(self.rect.x)
            hit_wall = True
        if self.rect.right > world_width:
            self.rect.right = world_width
            self.x = float(self.rect.x)
            hit_wall = True
        if hit_wall:
            self.direction *= -1

        self.vy += ENEMY_GRAVITY * dt
        self.y += self.vy * dt
        self.rect.y = int(self.y)
        self.on_ground = False

        for tile in solid_tiles:
            if not self.rect.colliderect(tile):
                continue
            if self.vy > 0:
                self.rect.bottom = tile.top
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = tile.bottom
            self.vy = 0.0
            self.y = float(self.rect.y)

        if self.rect.bottom > world_height:
            self.rect.bottom = world_height
            self.y = float(self.rect.y)
            self.vy = 0.0
            self.on_ground = True

        if not hit_wall and self.on_ground:
            front_x = self.rect.right + 1 if self.direction > 0 else self.rect.left - 1
            front_probe = pygame.Rect(front_x, self.rect.bottom + 1, 1, 1)
            has_ground_ahead = False
            for tile in solid_tiles:
                if front_probe.colliderect(tile):
                    has_ground_ahead = True
                    break
            if not has_ground_ahead:
                self.direction *= -1

    def draw(self, surface: pygame.Surface, screen_rect: pygame.Rect) -> None:
        if self.alive:
            pygame.draw.rect(surface, ENEMY_COLOR, screen_rect)
