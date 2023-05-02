from utils.constants import *


class Piece:
    PADDING = 10    # Espaco entre as pecas
    PIECE_RADIUS = SQUARE_SIZE // 2 - PADDING   # Raio da peca

    def __init__(self, row, col, color):
        '''
        Inicializa um objeto peça.
        :param row: A linha da peça.
        :param col: A coluna da peça.
        :param color: A cor da peça.
        '''
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def move(self, row, col):
        """
        Move a peça para a linha e coluna indicadas.
        :param A linha para onde mover.
        :param col: A coluna para onde mover.
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.PIECE_RADIUS)
        if self.king:
            screen.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def __repr__(selfs):
        """
        Permite ver que peça está a ser apontada. Retornando a posicao da peca
        """
        return "Piece: " + str(selfs.row) + ", " + str(selfs.col) + ", " + str(selfs.color)
