import pygame
import random

# 初始化 pygame
pygame.init()

# 游戏配置
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128), 
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]

# 方块形状定义 (4x4 矩阵)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]], # Z
    [[1, 0, 0], [1, 1, 1]], # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def get_matrix(self):
        # 旋转矩阵逻辑
        res = self.shape
        for _ in range(self.rotation):
            res = [list(row) for row in zip(*res[::-1])]
        return res

def check_collision(board, piece, offset_x, offset_y, rotation=None):
    if rotation is None: rotation = piece.rotation
    # 获取旋转后的形状
    temp_piece = Piece(piece.x, piece.y, piece.shape)
    temp_piece.rotation = rotation
    matrix = temp_piece.get_matrix()
    
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val:
                new_x = piece.x + c + offset_x
                new_y = piece.y + r + offset_y
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                    return True
                if new_y >= 0 and board[new_y][new_x]:
                    return True
    return False

def clear_lines(board):
    lines_cleared = 0
    new_board = [row for row in board if any(val == 0 for val in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLUMNS)
    return new_board, lines_cleared

def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python 俄罗斯方块")
    clock = pygame.time.Clock()
    
    board = [[0] * COLUMNS for _ in range(ROWS)]
    current_piece = Piece(COLUMNS // 2 - 1, 0, random.choice(SHAPES))
    score = 0
    fall_time = 0
    fall_speed = 500 # 初始下落速度 (毫秒)
    
    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        # 自动下落逻辑
        if fall_time > fall_speed:
            if not check_collision(board, current_piece, 0, 1):
                current_piece.y += 1
            else:
                # 落地，固定方块
                matrix = current_piece.get_matrix()
                for r, row in enumerate(matrix):
                    for c, val in enumerate(row):
                        if val:
                            board[current_piece.y + r][current_piece.x + c] = current_piece.color
                board, cleared = clear_lines(board)
                score += cleared * 100
                current_piece = Piece(COLUMNS // 2 - 1, 0, random.choice(SHAPES))
                # 检查游戏结束
                if check_collision(board, current_piece, 0, 0):
                    running = False
            fall_time = 0

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(board, current_piece, -1, 0):
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(board, current_piece, 1, 0):
                    current_piece.x += 1
                if event.key == pygame.K_DOWN and not check_collision(board, current_piece, 0, 1):
                    current_piece.y += 1
                if event.key == pygame.K_UP:
                    new_rot = (current_piece.rotation + 1) % 4
                    if not check_collision(board, current_piece, 0, 0, new_rot):
                        current_piece.rotation = new_rot

        # 绘制背景网格
        draw_grid(screen)

        # 绘制已固定的方块
        for y, row in enumerate(board):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制当前掉落的方块
        matrix = current_piece.get_matrix()
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, current_piece.color, 
                                     ((current_piece.x + c) * BLOCK_SIZE, (current_piece.y + r) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        pygame.display.flip()

    print(f"游戏结束！最终得分: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()