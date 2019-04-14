REVERSI_PACKAGES = {
    'EMPTY': 0,
    'WHITE': 1,
    'BLACK': -1,
    'DRAW': 2,
    'ERROR': -999,
    'EDGE_PAD': -999,
    'SQUARE_NUM': 64,
    'SIDES_NUM': 8,
    'CHANGE_COLOR': -1,
    'ALL_VECTORS': [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]],
    'VECTOR_NUM': 8,
    'INITIAL_REVERSIBLE_STONE_NUMBER_LIST': [0, 0, 0, 0, 0, 0, 0, 0],
    'INITIAL_WHITE_PLACES': [27, 36],
    'INITIAL_BLACK_PLACES': [28, 35]
}

DQN = {
    'model1': 'utils/dqn_models/model1/model1.pt'
}

MARKS = {
    '0': ' ',
    '1': '⚪️',
    '-1': '⚫️',
    '2': '☆'
}
