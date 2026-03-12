import random
import sys

import pygame


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
FPS = 10


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 40, 40)


def random_food_position(snake_body):
    while True:
        position = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if position not in snake_body:
            return position


def draw_cell(surface, color, position):
    rect = pygame.Rect(
        position[0] * CELL_SIZE,
        position[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )
    pygame.draw.rect(surface, color, rect)


def draw_score(surface, font, score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def game_over_screen(surface, font, score):
    surface.fill(BLACK)
    line1 = font.render("Game Over", True, RED)
    line2 = font.render(f"Final Score: {score}", True, WHITE)
    line3 = font.render("Press ESC or close window", True, WHITE)

    surface.blit(line1, (WINDOW_WIDTH // 2 - line1.get_width() // 2, 170))
    surface.blit(line2, (WINDOW_WIDTH // 2 - line2.get_width() // 2, 220))
    surface.blit(line3, (WINDOW_WIDTH // 2 - line3.get_width() // 2, 270))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    next_direction = direction
    food = random_food_position(snake)
    score = 0

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        next_direction = (1, 0)

        if not game_over:
            direction = next_direction
            head_x = snake[0][0] + direction[0]
            head_y = snake[0][1] + direction[1]
            new_head = (head_x, head_y)

            hit_wall = not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT)
            hit_self = new_head in snake

            if hit_wall or hit_self:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                else:
                    snake.pop()

            screen.fill(BLACK)
            draw_cell(screen, RED, food)
            for segment in snake:
                draw_cell(screen, GREEN, segment)
            draw_score(screen, font, score)
            pygame.display.flip()
            clock.tick(FPS)
        else:
            game_over_screen(screen, font, score)
            clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
