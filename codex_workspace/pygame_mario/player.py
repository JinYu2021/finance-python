import pygame

from settings import (
    PLAYER_COLOR,
    PLAYER_GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVE_SPEED,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
)


class Player:
    def __init__(self, start_x: float = 100.0, start_y: float = 0.0) -> None:
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        self.rect = pygame.Rect(int(start_x), int(start_y), PLAYER_WIDTH, PLAYER_HEIGHT)
        self.prev_rect = self.rect.copy()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.on_ground:
            self.vy = -PLAYER_JUMP_SPEED
            self.on_ground = False
            return True
        return False

    def respawn(self) -> None:
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.prev_rect = self.rect.copy()

    def bounce(self) -> None:
        self.vy = -PLAYER_JUMP_SPEED * 0.55
        self.on_ground = False

    def update(self, dt: float, solid_tiles: list[pygame.Rect], world_width: int, world_height: int) -> None:
        self.prev_rect = self.rect.copy()
        keys = pygame.key.get_pressed()
        move_dir = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_dir -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_dir += 1

        self.vx = move_dir * PLAYER_MOVE_SPEED
        self.x += self.vx * dt
        self.rect.x = int(self.x)

        for tile in solid_tiles:
            if not self.rect.colliderect(tile):
                continue
            if self.vx > 0:
                self.rect.right = tile.left
            elif self.vx < 0:
                self.rect.left = tile.right
            self.x = float(self.rect.x)

        self.vy += PLAYER_GRAVITY * dt
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

        if self.rect.left < 0:
            self.rect.left = 0
            self.x = float(self.rect.x)
        if self.rect.right > world_width:
            self.rect.right = world_width
            self.x = float(self.rect.x)

        if self.rect.bottom > world_height:
            self.rect.bottom = world_height
            self.y = float(self.rect.y)
            self.vy = 0.0
            self.on_ground = True

    def draw(self, surface: pygame.Surface, screen_rect: pygame.Rect) -> None:
        pygame.draw.rect(surface, PLAYER_COLOR, screen_rect)
