import pygame
import random

pygame.init()

# Definição de cores:
Fuchsia = (255,0,255)
Purple = (255,69,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuração da janela do jogo:
WIDTH = 400  # Largura reduzida do tabuleiro
HEIGHT = 400  # Altura reduzida do tabuleiro
WINDOW_SIZE = (WIDTH, HEIGHT + 100)  # Altura aumentada para exibir o resultado
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Jogo da velha")

# Configuração da fonte:
font = pygame.font.Font(None, 60)

# Variáveis globais do jogo:
board = [' '] * 9
player_turn = 'O'
game_over = False

# Função responsável por desenhar o tabuleiro na tela
def draw_board():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 5)
    pygame.draw.line(screen, WHITE, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 5)
    pygame.draw.line(screen, WHITE, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)

    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            if board[index] == 'O':
                circle_center_x = j * WIDTH // 3 + WIDTH // 6
                circle_center_y = i * HEIGHT // 3 + HEIGHT // 6
                circle_radius = min(WIDTH // 8, HEIGHT // 8) - 10
                pygame.draw.circle(screen, Purple, (circle_center_x, circle_center_y), circle_radius, 5)
            elif board[index] == 'X':
                line_x1 = j * WIDTH // 3 + WIDTH // 12
                line_y1 = i * HEIGHT // 3 + HEIGHT // 12
                line_x2 = (j + 1) * WIDTH // 3 - WIDTH // 12
                line_y2 = (i + 1) * HEIGHT // 3 - HEIGHT // 12
                pygame.draw.line(screen, Fuchsia, (line_x1, line_y1), (line_x2, line_y2), 3)
                pygame.draw.line(screen, Fuchsia, (line_x2, line_y1), (line_x1, line_y2), 3)

    pygame.display.update()

# Verifica se o tabuleiro está completamente preenchido
def is_board_full(board):
    return ' ' not in board # Retorna True se estiver cheio e False caso contrário

# Verifica se o jogador atual venceu o jogo
def is_winner(board, player):
    # Verifica todas as condições de vitória possíveis: linhas, colunas e diagonais
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]  # Diagonais
    ]
    #Retorna True se o jogador vencer e False caso contrário
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Avalia o estado atual do tabuleiro
def evaluate(board):
    if is_winner(board, 'X'):
        return 1  # Verifica se jogador IA 'X' venceu, retornando 1
    elif is_winner(board, 'O'):
        return -1  # Verifica se o jogador humano 'O' venceu, retornando -1
    else:
        return 0  # Caso contrário, retorna 0, indicando empate

# Implementação do algoritmo minimax para determinar a melhor jogada para a IA

''' A função faz uma chamada recursiva para cada possível jogada e calcula a pontuação para cada jogada,
    retornando a melhor pontuação encontrada
'''
def minimax(board, depth, is_maximizing):
    # Verifica se o jogo já terminou (alguém venceu ou empate (tabuleiro cheio)) e retorna o valor de avaliação
    if is_winner(board, 'X'):
        return 1
    elif is_winner(board, 'O'):
        return -1
    elif is_board_full(board):
        return 0
    # Se is_maximizing for verdadeiro, representa a vez da IA (jogador 'X'), e a função procura a jogada que maximize a pontuação
    if is_maximizing:
        best_score = -float('inf')
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    # Se is_maximizing for falso, representa a vez do humano (jogador 'O'), e a função procura a jogada que minimize a pontuação
    else:
        best_score = float('inf')
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score
    
# Função para exibir o resultado final do jogo na tela

#Recebe como parâmetro o resultado do jogo: "win" (vitória do jogador), "loss" (vitória da IA) ou "draw" (empate)
def display_result(result):
    if result == "win":
        text = font.render("VOCÊ VENCEU! :)", True, (222,184,135))
    elif result == "loss":
        text = font.render("IA VENCEU! :’(", True, (222,184,135))
    else:
        text = font.render("EMPATE! >.<", True, (222,184,135))
    
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 50))  # Posiciona o texto abaixo do tabuleiro
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

# Função para fazer a jogada do humano (jogador 'O')
''' Use um loop para esperar pelo evento de clique do mouse; obtém as coordenadas do clique e convert para as coordenadas da matriz do tabuleiro;
    verifica se a posição escolhida está vazia e faz a jogada; atualizara a tela e verifica se o jogo terminou; Após o término do jogo, 
    aguarde o evento de fechamento da janela para fechar o programa'''
def make_player_move():
    global game_over, player_turn
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if player_turn == 'O':
                col = event.pos[0] // (WIDTH // 3)
                row = event.pos[1] // (HEIGHT // 3)
                index = row * 3 + col
                if board[index] == ' ':
                    board[index] = 'O'
                    draw_board()
                    if is_winner(board, 'O'):
                        display_result("win")
                        game_over = True
                    elif is_board_full(board):
                        display_result("draw")
                        game_over = True
                    else:
                        player_turn = 'X'
                        make_ai_move()
                        player_turn = 'O'
                        draw_board()
                        if is_winner(board, 'X'):
                            display_result("loss")
                            game_over = True
                        elif is_board_full(board):
                            display_result("draw")
                            game_over = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Função para fazer a jogada da IA (jogador 'X')
''' Percorre todas as posições vazias do tabuleiro e usando algoritmo minimax obtem a melhor jogada, 
    atualizando a posição escolhida com a marcação 'X' '''
def make_ai_move():
    best_score = -float('inf')
    best_move = -1
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    if best_move != -1:
        board[best_move] = 'X'

# Loop principal do jogo
draw_board() # desenhar o tabuleiro na tela
make_player_move() # inicia o jogo