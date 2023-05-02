import pygame
from checkers.actions import Actions
from checkers.board import Board
from utils.constants import *
from minimax.minimax_algo import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DAMAS")


def get_pos_from_mouse(pos):
    """
    Retorna a posição do mouse no quadro
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    """
    Função principal do programa

    """
    clock = pygame.time.Clock()
    run = True
    actions = Actions(WIN)
    board = Board()

    while run:
        clock.tick(FPS)

        if actions.turn == RED:
            value, new_board = minimax(actions.get_board(), 3, True, actions)           # Uma maior profundidade significa que a IA pode
                                                                                        # olhar mais à frente, mas será significativamente
                                                                                        # mais lenta.
            actions.minimax_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)
                if actions.turn:
                    actions.select(row, col)
        actions.check_for_draw()

        actions.update()


main()
