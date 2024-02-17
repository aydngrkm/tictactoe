import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """ Returns starting state of the board. """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """ Returns player who has the next turn on a board. """
    xCount = 0
    oCount = 0

    for l in board:
        for i in l:
            if i == X:
                xCount += 1
            elif i == O:
                oCount += 1
    if oCount == xCount:
        return X

    return O

def actions(board):
    """ Returns set of all possible actions (i, j) available on the board. """
    acts = set()
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                acts.add((i, j))

    return acts



def result(board, action):
    """ Returns the board that results from making move (i, j) on the board. """
    if board[action[0]][action[1]]:
        raise Exception("Action is not possible.")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    
    return new_board


def winner(board):
    """ Returns the winner of the game, if there is one. """
    if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        return board[0][0]
    if board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        return board[1][0]
    if board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        return board[2][0]
    if board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    if board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    if board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]


def terminal(board):
    """ Returns True if game is over, False otherwise. """
    if winner(board) or len(actions(board)) == 0:
        return True
    
    return False


def utility(board):
    """ Returns 1 if X has won the game, -1 if O has won, 0 otherwise. """
    pl_who_won = winner(board)
    if pl_who_won == X:
        return 1
    elif pl_who_won == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)
        
    v = -math.inf

    for act in actions(board):
        v = max(v, min_value(result(board, act)))

    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = math.inf

    for act in actions(board):
        v = min(v, max_value(result(board, act)))

    return v

def minimax(board):
    """ Returns the optimal action for AI on the board. """
    if terminal(board):
        return None
    
    curr_pl = player(board)
    acts = list(actions(board))
    best_move = acts[0]

    if curr_pl == X:
        for act in acts:
            if min_value(result(board, act)) > min_value(result(board, best_move)):
                best_move = act

        return best_move
    
    if curr_pl == O:
        for act in acts:
            if max_value(result(board, act)) < max_value(result(board, best_move)):
                best_move = act

        return best_move
