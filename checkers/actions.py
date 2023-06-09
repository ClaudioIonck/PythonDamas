from utils.constants import *
from checkers.board import Board


class Actions:
    def __init__(self, screen):
        self._init()
        self.screen = screen
        self.selected = None
        self.valid_moves = {}

    def update(self):
        if self.board is not None:
            self.board.draw(self.screen)
            self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLUE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            output_pos = self._move(row, col)
            if not output_pos:  # se o movimento for inválido
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn: # movimento valido
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def check_for_draw(self):
        pieces = self.board.get_all_pieces(self.turn)
        possible_moves = []
        for piece in pieces:
            possible_moves.append(self.board.get_valid_moves(piece))

        if not any(possible_moves): # se nao tiver mais movimentos jogo acaba
            print(f"O jogo terminou empatado porque {self.turn} não tem mais movimentos.")
            pygame.quit()
            exit()

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove_piece(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                    row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

    def get_board(self):
        return self.board

    def minimax_move(self, board):
        self.board = board
        self.change_turn()
