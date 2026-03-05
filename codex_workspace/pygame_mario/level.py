import csv
from pathlib import Path

import pygame

from settings import TILE_COLOR, TILE_SIZE, WIDTH


class Level:
    def __init__(self, csv_path: str) -> None:
        self.grid = self._load_grid(csv_path)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        self.world_width = self.cols * TILE_SIZE
        self.world_height = self.rows * TILE_SIZE
        self.solid_tiles: list[pygame.Rect] = []
        self._build_solid_tiles()

    def _load_grid(self, csv_path: str) -> list[list[int]]:
        path = Path(csv_path)
        rows: list[list[int]] = []

        with path.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for raw_row in reader:
                if not raw_row:
                    continue
                row = [int(cell.strip()) for cell in raw_row]
                rows.append(row)

        if not rows:
            raise ValueError(f"Level CSV is empty: {csv_path}")

        width = len(rows[0])
        for row in rows:
            if len(row) != width:
                raise ValueError(f"Inconsistent row width in level CSV: {csv_path}")

        return rows

    def _build_solid_tiles(self) -> None:
        for row_idx, row in enumerate(self.grid):
            for col_idx, value in enumerate(row):
                if value == 1:
                    rect = pygame.Rect(
                        col_idx * TILE_SIZE,
                        row_idx * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE,
                    )
                    self.solid_tiles.append(rect)

    def draw(self, surface: pygame.Surface, camera) -> None:
        for world_rect in self.solid_tiles:
            screen_rect = camera.world_to_screen_rect(world_rect)
            if screen_rect.right < 0 or screen_rect.left > WIDTH:
                continue
            pygame.draw.rect(surface, TILE_COLOR, screen_rect)
