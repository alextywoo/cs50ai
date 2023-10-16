"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):

    count_X, count_O = 0, 0

    for rows in board:
        for cell in rows:
            if cell == X:
                count_X += 1
            elif cell == O:
                count_O += 1

    if not terminal(board) and count_X == count_O:
        return X
    elif count_X > count_O:
        return O
    """
    Returns player who has the next turn on a board.
    """


def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):

    new_board = copy.deepcopy(board)


    if not is_valid_action(new_board, action):
        raise Exception("Invalid action")


    mark = player(board)
    x, y = action
    new_board[x][y] = mark

    return new_board

    """
    Returns the board that results from making move (i, j) on the board.
    """

def is_valid_action(board, action):

    open_positions = actions(board)

    if action not in open_positions:
        return False
    else:
        return True

def winner(board):

    # Check rows for a win
    for row in board:
        if row == ["X", "X", "X"]:
            return X
        elif row == ["O", "O", "O"]:
            return O

    # Check columns for a win
    for col in range(3):
        if all(board[row][col] == "X" for row in range(3)):
            return X
        elif all(board[row][col] == "O" for row in range(3)):
            return O

    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O

    # No winner
    return None

    """
    Returns the winner of the game, if there is one.
    """


def terminal(board):
    # Check for a winner
    if winner(board) is not None:
        return True

    # Check for a tie (if the board is full)
    if all(cell != EMPTY for row in board for cell in row):
        return True

    # If neither condition is met, the game is still in progress
    return False


def utility(board):
    # Check if the board has a winner
    winner_player = winner(board)

    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1

    else:
        return 0



def minimax(board):

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    if terminal(board):
        return None

    if player(board) == X:
        optimal_value = float('-inf')
        optimal_action = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > optimal_value:
                optimal_value = value
                optimal_action = action
        return optimal_action

    else:
        optimal_value = float('inf')
        optimal_action = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < optimal_value:
                optimal_value = value
                optimal_action = action
        return optimal_action



    """
    Returns the optimal action for the current player on the board.
    """