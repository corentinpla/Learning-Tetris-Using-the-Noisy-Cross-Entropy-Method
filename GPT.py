import numpy as np

# Define the board dimensions
ROWS = 20
COLS = 10

# Define the piece shapes and rotations
SHAPES = np.array([
    # I
    [[1, 1, 1, 1],[1],],
    
    # J
    [[0, 0, 1],
     [1, 1, 1]],
    
    # L
    [[1, 0, 0],
     [1, 1, 1]],
    
    # O
    [[1, 1],
     [1, 1]],
    
    # S
    [[0, 1, 1],
     [1, 1, 0]],
    
    # T
    [[0, 1, 0],
     [1, 1, 1]],
    
    # Z
    [[1, 1, 0],
     [0, 1, 1]]
])

# Define the initial board state
board = np.zeros((ROWS, COLS), dtype=int)

# Define the scoring heuristics
weights = np.array([
    -0.51, 0.76, -0.36, -0.18, 
    0.71, -0.22, -0.32
])

def evaluate_position(board, piece, rotation, column):
    # Copy the board and add the piece to it
    test_board = np.copy(board)
    test_piece = SHAPES[piece][rotation]
    height = test_piece.shape[0]
    width = test_piece.shape[1]
    row = 0
    for r in range(height):
        for c in range(width):
            if test_piece[r][c] == 1:
                test_board[row][column + c] = piece + 1
        row += 1
    
    # Compute the score using the heuristics
    heights = [ROWS - max(test_board[:, c]) for c in range(COLS)]
    diffs = [abs(h1 - h2) for h1, h2 in zip(heights[:-1], heights[1:])]
    score = np.dot(weights, [heights[3], max(heights), sum(diffs), min(heights), heights[1], heights[2], heights[3]])
    
    return score

def get_best_move(board, piece, column):
    # Find the best rotation and column for the current piece
    best_rotation = 0
    best_score = -np.inf
    for r in range(len(SHAPES[piece])):
        for c in range(column - 2, column + 3):
            if c < 0 or c + SHAPES[piece][r].shape[1] > COLS:
                continue
            score = evaluate_position(board, piece, r, c)
            if score > best_score:
                best_score = score
                best_rotation = r
                best_column = c
    
    return best_rotation, best_column

def place_piece(board, piece, rotation, column):
    # Add the piece to the board
    test_board = np.copy(board)
    test_piece = SHAPES[piece][rotation]
    height = test_piece.shape[0]
    width = test_piece.shape[1]
    row = 0
    for r in range(height):
        for c in range(width):
            if test_piece
