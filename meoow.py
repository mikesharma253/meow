import pygame
import random

pygame.init()

# Screen
WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slow Tetris")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 1, 0],
     [0, 1, 1]]
]

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]

    for (x, y), color in locked_positions.items():
        grid[y][x] = color

    return grid

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, GRAY,
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def valid_space(piece, grid):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                if (x + piece.x < 0 or
                    x + piece.x >= WIDTH // BLOCK_SIZE or
                    y + piece.y >= HEIGHT // BLOCK_SIZE or
                    grid[y + piece.y][x + piece.x] != BLACK):
                    return False
    return True

def lock_piece(piece, locked):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                locked[(x + piece.x, y + piece.y)] = piece.color

def clear_rows(grid, locked):
    cleared = 0
    for y in range(len(grid)-1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            for x in range(len(grid[y])):
                del locked[(x, y)]

            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, ky = key
                if ky < y:
                    locked[(x, ky + 1)] = locked.pop(key)
    return cleared

def main():
    locked_positions = {}
    current_piece = Piece()
    fall_time = 0

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # 🔥 Slow falling speed (increase value = slower)
        if fall_time > 700:
            current_piece.y += 1
            fall_time = 0
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                lock_piece(current_piece, locked_positions)
                current_piece = Piece()
                clear_rows(grid, locked_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        screen.fill(BLACK)
        draw_grid(screen, grid)

        # Draw current piece
        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece.color,
                        ((current_piece.x + x) * BLOCK_SIZE,
                         (current_piece.y + y) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()

    pygame.quit()

main()