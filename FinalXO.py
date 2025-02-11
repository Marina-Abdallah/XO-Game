import pygame

# colors
BG = (232, 220, 202)
LINE_COLOR =  (128, 0, 128)
X_COLOR = (242, 85, 96)
O_COLOR = (28, 170, 156)

# Game setting
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

# size of game board
WIDTH = 400
HEIGHT = 500
LINE_WIDTH = 5
CELL_WIDTH= WIDTH//3
CELL_HIGHT = HEIGHT//3


pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final_XO")


def draw_board(board):
    for row in range(1, 3):
        #draw row lines
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_HIGHT), (WIDTH, row * CELL_HIGHT), LINE_WIDTH)
    for col in range(1, 3):
        #draw colum lines
        pygame.draw.line(screen, LINE_COLOR, (col * CELL_WIDTH, 0), (col * CELL_WIDTH, HEIGHT), LINE_WIDTH)
    
    # draw x & o in cells
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                #\
                pygame.draw.line(screen, X_COLOR,(col*CELL_WIDTH +30,row*CELL_HIGHT +30),((col+1)*CELL_WIDTH-30,(row+1)*CELL_HIGHT-30), 8)
                #/
                pygame.draw.line(screen, X_COLOR, ((col+1)*CELL_WIDTH-30, row*CELL_HIGHT +30), 
                               (col*CELL_WIDTH+30, (row+1)*CELL_HIGHT -30), 8)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (col * CELL_WIDTH+ CELL_WIDTH // 2, row * CELL_HIGHT + CELL_HIGHT// 2), (CELL_WIDTH-30)//2, 8)

def blur_surface(surface, scale_factor=8):
    #Simulates a blur effect by scaling down and up the surface.
    width, height = surface.get_size()
    small_surface = pygame.transform.smoothscale(surface, (width // scale_factor, height // scale_factor))
    blurred_surface = pygame.transform.smoothscale(small_surface, (width, height))
    return blurred_surface


def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

#list of all available moves (empty cells) on the board
def available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

# Minimax Algoruthm
#is_maximizing indicating whether the algorithm is trying to
# maximize (AI's turn) or minimize (PLAYER's turn) the score.
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == AI:
        return 1
    elif winner == PLAYER:
        return -1
    #game is a tie
    elif not available_moves(board):
        return 0
    
    #AI turn
    if is_maximizing:
        #negative infinity
        best_score = -float('inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = AI
            #Player turn
            score = minimax(board, False)
            board[move[0]][move[1]] = EMPTY
            best_score = max(score, best_score)
        return best_score
    #Player turn
    else:
        best_score = float('inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = PLAYER
            #AI turn
            score = minimax(board, True)
            board[move[0]][move[1]] = EMPTY
            best_score = min(score, best_score)
        return best_score

#the optimal move for the AI using the Minimax Algorithm
def best_move(board):
    best_score = -float('inf')
    move = None
    for available_move in available_moves(board):
        board[available_move[0]][available_move[1]] = AI
        score = minimax(board, False)
        board[available_move[0]][available_move[1]] = EMPTY
        if score > best_score:
            best_score = score
            move = available_move
    return move


def play_game():
    board = [[EMPTY] * 3 for _ in range(3)]
    running = True
    turn = PLAYER 
    winner = None  # To store the winner
    final_display = False
    blurred_background = None

    while running:
        screen.fill(BG)
        draw_board(board)
        if not final_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = y // CELL_HIGHT
                    col = x // CELL_WIDTH
                    if board[row][col] == EMPTY and turn == PLAYER:
                        board[row][col] = PLAYER
                        if check_winner(board) == PLAYER:
                            winner="Player wins!!"
                            final_display = True
                        elif not available_moves(board):
                            winner = "It's a Tie!"
                            final_display = True
                        turn = AI

            #AI Turn
            if turn == AI and not final_display:
                ai_move = best_move(board)
                board[ai_move[0]][ai_move[1]] = AI
                if check_winner(board) == AI:
                    winner = "AI Wins!"
                    final_display = True
                elif not available_moves(board):
                    winner = "It's a Tie!"
                    final_display = True
                turn = PLAYER
    
        else:
            if blurred_background is None:
                # Create a blurred version of the current screen
                blurred_background = blur_surface(screen)
            screen.blit(blurred_background, (0, 0))
            # Display the result
            font = pygame.font.Font(None, 80)
            text = font.render(winner, True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

            #Restart button
            button=pygame.draw.rect(screen, LINE_COLOR, (WIDTH // 3 , HEIGHT // 2 + 50, 135, 50))
            font = pygame.font.Font(None, 40)
            text_surface = font.render("Restart", True, (255,255,255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2 , HEIGHT // 2 + 75))
            screen.blit(text_surface, text_rect) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        # Reset the game
                        board = [[EMPTY] * 3 for _ in range(3)]
                        turn = PLAYER
                        winner = None
                        final_display = False
                        blurred_background = None
        pygame.display.update()

    pygame.quit()

#start game
play_game()