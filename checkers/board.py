from utils.constants import *
from .piece import Piece


class Board:
    def __init__(self):
        """
        Inicia o tabuleiro.
        """
        self.board = []
        self.blue_left = self.red_left = 12
        self.blue_kings = self.red_kings = 0
        self.create_board()
        self.run = True

    def draw_grid(self, screen):
        """
        Desanha o tabuleiro.
        :param screen: Como ele vai fazer o tabuleiro.
        """
        screen.fill(BLACK)
        for row in range(HEIGHT):
            for col in range(row % 2, NUM_ROWS, 2):
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        """
        Vai mover a peca para a nova posicao.
        :param piece: Mover a peca.
        :param row: A linha para onde mover.
        :param col: A coluna para onde mover.
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == 0 or row == NUM_ROWS - 1:
            if piece.color == RED and not piece.king:
                self.red_kings += 1
                piece.make_king()
            if piece.color == BLUE and not piece.king:
                self.blue_kings += 1
                piece.make_king()

    def evaluate(self):
        """
        Mostra a pontuacao da partida.
        :return: Mostra a pontuacao atual.
        """
        return self.red_left - 2 * self.blue_left + (self.red_kings * 0.03 - self.blue_kings * 0.05)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces

    def get_piece(self, row, col):
        """
        Vai obter a peca determinada na posicao.
        :param row: A linha da peca.
        :param col: A coluna da peca.
        :return: A peca na posicao.
        """
        return self.board[row][col]

    def create_board(self):
        """
        Cria o tabuleiro.
        """
        for row in range(NUM_ROWS):
            self.board.append([])
            for col in range(NUM_COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLUE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen):
        """
        Mostra as pecas na tela
        :param screen: A tela on vai desenhar.
        """
        self.draw_grid(screen)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def remove_piece(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLUE:
                    self.blue_left -= 1
                else:
                    self.red_left -= 1

                print(self.blue_left, self.red_left)
                if self.winner() is not None:
                    print("O vencedor foi: " + str(self.winner()))
                    pygame.quit()
                    exit()

    def winner(self):
        if self.blue_left == 0:
            return "Vermelho"
        elif self.red_left == 0:
            return "Azul"
        else:
            return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLUE or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, NUM_ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, NUM_ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            potential_move = self.board[r][left]
            if potential_move == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last  # Se a jogada for valida, ele adiciona como uma jogada valida

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, NUM_ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break

            elif potential_move.color == color:
                break
            else:
                last = [potential_move]  # Se a peca matar outra peca e se tiver a possibilidade de matar outra ajustar a lista
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= NUM_COLS:
                break

            potential_move = self.board[r][right]
            if potential_move == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last  # Se uma jogada for valida ele adiciona a lista de jogadas validas.

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, NUM_ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            elif potential_move.color == color:
                break
            else:
                last = [potential_move]  # Se apos uma jogada conseguir realizar outra jogada ajustar a ultima peca da lista.
            right += 1

        return moves
