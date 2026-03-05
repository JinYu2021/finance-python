import random
import sys
import pygame

# ------------------------
# Basic game configuration
# ------------------------
CELL_SIZE = 30
COLS = 10
ROWS = 20
PLAY_WIDTH = COLS * CELL_SIZE
PLAY_HEIGHT = ROWS * CELL_SIZE
SIDE_PANEL = 220
WINDOW_WIDTH = PLAY_WIDTH + SIDE_PANEL
WINDOW_HEIGHT = PLAY_HEIGHT
FPS = 60
DROP_INTERVAL_MS = 500

# Colors
BLACK = (18, 18, 18)
BG = (28, 28, 36)
GRID = (48, 48, 60)
WHITE = (240, 240, 240)
GRAY = (160, 160, 160)

SHAPE_COLORS = {
    "I": (0, 240, 240),
    "O": (240, 240, 0),
    "T": (160, 0, 240),
    "S": (0, 240, 0),
    "Z": (240, 0, 0),
    "J": (0, 0, 240),
    "L": (240, 160, 0),
}

# Tetromino definitions in 4x4 matrices
SHAPES = {
    "I": [
        [
            "....",
            "XXXX",
            "....",
            "....",
        ],
        [
            "..X.",
            "..X.",
            "..X.",
            "..X.",
        ],
    ],
    "O": [
        [
            ".XX.",
            ".XX.",
            "....",
            "....",
        ]
    ],
    "T": [
        [
            ".X..",
            "XXX.",
            "....",
            "....",
        ],
        [
            ".X..",
            ".XX.",
            ".X..",
            "....",
        ],
        [
            "....",
            "XXX.",
            ".X..",
            "....",
        ],
        [
            ".X..",
            "XX..",
            ".X..",
            "....",
        ],
    ],
    "S": [
        [
            ".XX.",
            "XX..",
            "....",
            "....",
        ],
        [
            ".X..",
            ".XX.",
            "..X.",
            "....",
        ],
    ],
    "Z": [
        [
            "XX..",
            ".XX.",
            "....",
            "....",
        ],
        [
            "..X.",
            ".XX.",
            ".X..",
            "....",
        ],
    ],
    "J": [
        [
            "X...",
            "XXX.",
            "....",
            "....",
        ],
        [
            ".XX.",
            ".X..",
            ".X..",
            "....",
        ],
        [
            "....",
            "XXX.",
            "..X.",
            "....",
        ],
        [
            ".X..",
            ".X..",
            "XX..",
            "....",
        ],
    ],
    "L": [
        [
            "..X.",
            "XXX.",
            "....",
            "....",
        ],
        [
            ".X..",
            ".X..",
            ".XX.",
            "....",
        ],
        [
            "....",
            "XXX.",
            "X...",
            "....",
        ],
        [
            "XX..",
            ".X..",
            ".X..",
            "....",
        ],
    ],
}


class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.rotations = SHAPES[kind]
        self.rotation = 0
        self.x = COLS // 2 - 2
        self.y = -1
        self.color = SHAPE_COLORS[kind]

    @property
    def matrix(self):
        return self.rotations[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.rotations)

    def rotate_back(self):
        self.rotation = (self.rotation - 1) % len(self.rotations)


def create_grid(locked):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (x, y), color in locked.items():
        if 0 <= y < ROWS and 0 <= x < COLS:
            grid[y][x] = color
    return grid


def get_piece_cells(piece):
    cells = []
    for r in range(4):
        for c in range(4):
            if piece.matrix[r][c] == "X":
                cells.append((piece.x + c, piece.y + r))
    return cells


def valid_position(piece, grid):
    for x, y in get_piece_cells(piece):
        if x < 0 or x >= COLS or y >= ROWS:
            return False
        if y >= 0 and grid[y][x] != BLACK:
            return False
    return True


def lock_piece(piece, locked):
    for x, y in get_piece_cells(piece):
        if y >= 0:
            locked[(x, y)] = piece.color


def clear_lines(locked):
    full_rows = []
    for y in range(ROWS):
        if all((x, y) in locked for x in range(COLS)):
            full_rows.append(y)

    if not full_rows:
        return 0

    for y in full_rows:
        for x in range(COLS):
            locked.pop((x, y), None)

    # Move rows above down
    shift = 0
    for y in range(ROWS - 1, -1, -1):
        if y in full_rows:
            shift += 1
        elif shift > 0:
            for x in range(COLS):
                if (x, y) in locked:
                    locked[(x, y + shift)] = locked.pop((x, y))

    return len(full_rows)


def score_for_lines(lines):
    return {1: 100, 2: 300, 3: 500, 4: 800}.get(lines, 0)


def random_piece():
    return Piece(random.choice(list(SHAPES.keys())))


def draw_grid(surface):
    for x in range(COLS + 1):
        pygame.draw.line(surface, GRID, (x * CELL_SIZE, 0), (x * CELL_SIZE, PLAY_HEIGHT), 1)
    for y in range(ROWS + 1):
        pygame.draw.line(surface, GRID, (0, y * CELL_SIZE), (PLAY_WIDTH, y * CELL_SIZE), 1)


def draw_board(surface, grid):
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x]
            pygame.draw.rect(
                surface,
                color,
                pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            if color != BLACK:
                pygame.draw.rect(
                    surface,
                    (30, 30, 30),
                    pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    1,
                )


def draw_piece(surface, piece):
    for x, y in get_piece_cells(piece):
        if y >= 0:
            pygame.draw.rect(
                surface,
                piece.color,
                pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(
                surface,
                (30, 30, 30),
                pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )


def draw_next(surface, piece, font):
    panel_x = PLAY_WIDTH + 20
    title = font.render("Next", True, WHITE)
    surface.blit(title, (panel_x, 20))

    for r in range(4):
        for c in range(4):
            if piece.matrix[r][c] == "X":
                x = panel_x + c * CELL_SIZE
                y = 60 + r * CELL_SIZE
                pygame.draw.rect(surface, piece.color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, (30, 30, 30), (x, y, CELL_SIZE, CELL_SIZE), 1)


def draw_ui(surface, score, level, paused, game_over, font, small_font):
    panel_x = PLAY_WIDTH + 20
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    ctrl1 = small_font.render("A/D or <- -> : Move", True, GRAY)
    ctrl2 = small_font.render("W or Up      : Rotate", True, GRAY)
    ctrl3 = small_font.render("S or Down    : Soft drop", True, GRAY)
    ctrl4 = small_font.render("Space        : Hard drop", True, GRAY)
    ctrl5 = small_font.render("P            : Pause", True, GRAY)
    ctrl6 = small_font.render("R            : Restart", True, GRAY)

    surface.blit(score_text, (panel_x, 220))
    surface.blit(level_text, (panel_x, 260))
    surface.blit(ctrl1, (panel_x, 330))
    surface.blit(ctrl2, (panel_x, 355))
    surface.blit(ctrl3, (panel_x, 380))
    surface.blit(ctrl4, (panel_x, 405))
    surface.blit(ctrl5, (panel_x, 430))
    surface.blit(ctrl6, (panel_x, 455))

    if paused:
        text = font.render("Paused", True, WHITE)
        rect = text.get_rect(center=(PLAY_WIDTH // 2, PLAY_HEIGHT // 2))
        surface.blit(text, rect)

    if game_over:
        text1 = font.render("Game Over", True, (255, 120, 120))
        text2 = small_font.render("Press R to restart", True, WHITE)
        rect1 = text1.get_rect(center=(PLAY_WIDTH // 2, PLAY_HEIGHT // 2 - 20))
        rect2 = text2.get_rect(center=(PLAY_WIDTH // 2, PLAY_HEIGHT // 2 + 15))
        surface.blit(text1, rect1)
        surface.blit(text2, rect2)


def reset_game():
    locked = {}
    current = random_piece()
    nxt = random_piece()
    score = 0
    level = 1
    lines_total = 0
    paused = False
    game_over = False
    return locked, current, nxt, score, level, lines_total, paused, game_over


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris (Python + Pygame)")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 28)
    small_font = pygame.font.SysFont("consolas", 20)

    (
        locked,
        current,
        nxt,
        score,
        level,
        lines_total,
        paused,
        game_over,
    ) = reset_game()

    drop_timer = 0

    running = True
    while running:
        dt = clock.tick(FPS)

        drop_speed = max(70, DROP_INTERVAL_MS - (level - 1) * 35)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    (
                        locked,
                        current,
                        nxt,
                        score,
                        level,
                        lines_total,
                        paused,
                        game_over,
                    ) = reset_game()
                    drop_timer = 0
                    continue

                if event.key == pygame.K_p and not game_over:
                    paused = not paused
                    continue

                if paused or game_over:
                    continue

                if event.key in (pygame.K_a, pygame.K_LEFT):
                    current.x -= 1
                    if not valid_position(current, create_grid(locked)):
                        current.x += 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    current.x += 1
                    if not valid_position(current, create_grid(locked)):
                        current.x -= 1
                elif event.key in (pygame.K_w, pygame.K_UP):
                    current.rotate()
                    if not valid_position(current, create_grid(locked)):
                        current.rotate_back()
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    current.y += 1
                    if not valid_position(current, create_grid(locked)):
                        current.y -= 1
                elif event.key == pygame.K_SPACE:
                    while True:
                        current.y += 1
                        if not valid_position(current, create_grid(locked)):
                            current.y -= 1
                            break

        if not running:
            break

        if not paused and not game_over:
            drop_timer += dt
            if drop_timer >= drop_speed:
                drop_timer = 0
                current.y += 1
                if not valid_position(current, create_grid(locked)):
                    current.y -= 1
                    lock_piece(current, locked)
                    lines = clear_lines(locked)
                    score += score_for_lines(lines)
                    lines_total += lines
                    level = 1 + lines_total // 10

                    current = nxt
                    nxt = random_piece()

                    if not valid_position(current, create_grid(locked)):
                        game_over = True

        grid = create_grid(locked)

        screen.fill(BG)
        pygame.draw.rect(screen, BLACK, (0, 0, PLAY_WIDTH, PLAY_HEIGHT))
        draw_board(screen, grid)
        if not game_over:
            draw_piece(screen, current)
        draw_grid(screen)

        draw_next(screen, nxt, font)
        draw_ui(screen, score, level, paused, game_over, font, small_font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
