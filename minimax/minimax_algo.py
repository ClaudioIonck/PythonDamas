from copy import deepcopy


BLUE = (0, 0, 255)  # Pecas do jogador principal
RED = (255, 0, 0)   # Pecas da IA


def minimax(position, depth, is_maximizing, game):
    """
    Algoritimo Minimax para o jogo de damas.
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for child in get_children(position, RED, game):
            score = minimax(child, depth - 1, False, game)[0]
            best_score = max(best_score, score)
            if best_score == score:
                best_move = child
        return best_score, best_move
    else:
        worst_score = float('inf')
        best_move = None
        for child in get_children(position, BLUE, game):
            score = minimax(child, depth - 1, True, game)[0]
            worst_score = min(worst_score, score)
            if worst_score == score:
                best_move = child
        return worst_score, best_move


def simulate_move(piece, move, board, skip):
    """
    Simula o movimento no tabuleiro
    """
    board.move(piece, move[0], move[1])
    if skip:
        board.remove_piece(skip)

    return board


def get_children(board, player, game):
    """
    Retorna a lista de todas as possiveis jogadas do jogador.
    """
    children = []
    for piece in board.get_all_pieces(player):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            children.append(new_board)
    return children
