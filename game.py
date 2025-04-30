import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 5
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
RADIUS = SQUARE_SIZE // 3
SPACE = SQUARE_SIZE // 5

# Colors
BG_COLOR = (32, 35, 100)
LINE_COLOR = (255, 255, 255)
CIRCLE_COLOR = (0, 255, 255)     # Neon blue
CROSS_COLOR = (255, 100, 180)    # Neon pink

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI - Color Edition")

# Game state
board = [["" for _ in range(COLS)] for _ in range(ROWS)]
player_turn = True
game_over = False

def draw_grid():
    screen.fill(BG_COLOR)
    for i in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                start1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                start2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

def available_moves():
    return [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] == ""]

def check_winner():
    for i in range(ROWS):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def is_draw():
    return all(cell != "" for row in board for cell in row) and not check_winner()

def minimax(is_maximizing):
    winner = check_winner()
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row, col in available_moves():
            board[row][col] = "O"
            score = minimax(False)
            board[row][col] = ""
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row, col in available_moves():
            board[row][col] = "X"
            score = minimax(True)
            board[row][col] = ""
            best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    best_move = None
    for row, col in available_moves():
        board[row][col] = "O"
        score = minimax(False)
        board[row][col] = ""
        if score > best_score:
            best_score = score
            best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = "O"

def reset_game():
    global board, player_turn, game_over
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    player_turn = True
    game_over = False
    draw_grid()
    draw_figures()
    pygame.display.update()

def show_game_over(result_text):
    font = pygame.font.SysFont(None, 40)
    text = font.render(result_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, 50))

    retry_rect = pygame.Rect(WIDTH//4 - 50, HEIGHT//2, 100, 40)
    exit_rect = pygame.Rect(3*WIDTH//4 - 50, HEIGHT//2, 100, 40)

    pygame.draw.rect(screen, (0, 200, 100), retry_rect)
    pygame.draw.rect(screen, (200, 50, 50), exit_rect)

    retry_text = font.render("Retry", True, (0, 0, 0))
    exit_text = font.render("Exit", True, (0, 0, 0))

    screen.blit(text, text_rect)
    screen.blit(retry_text, retry_text.get_rect(center=retry_rect.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    reset_game()
                    return
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Initial draw
draw_grid()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0] // SQUARE_SIZE
                y = event.pos[1] // SQUARE_SIZE
                if board[y][x] == "":
                    board[y][x] = "X"
                    player_turn = False

            if not player_turn and not game_over:
                ai_move()
                player_turn = True

            draw_figures()
            winner = check_winner()
            if winner or is_draw():
                game_over = True
                if winner == "X":
                    show_game_over("🎉 Congratulations! You win!")
                elif winner == "O":
                    show_game_over("😢 You lose!")
                else:
                    show_game_over("😐 It's a draw!")

    pygame.display.update()

#tic-tac-toe game
