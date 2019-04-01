import random

import numpy as np

from reversiTools.utils.reversi_packages import ReversiPackages


def intlist2strings(li):
    li = [str(fac) for fac in li]
    return ','.join(li)


def strings2intlist(strings):
    return strings.split(',')


def list2matrix(li):
    return np.array(li).reshape(8, 8).tolist()


def matrix2list(matrix):
    return np.array(matrix).reshape(1, -1).tolist()[0]


def get_simple_board(board):
    """
    get the board not using 2 and stone putable pos list from the board filled with 2
    :param board: list(int)
        shape = (1,64)
    :return: board: list(int)
                shape=(1,64)
            stone_putable_pos:list(int)
    """
    stone_putable_pos = []
    for index in range(len(board)):
        if board[index] == 2:
            board[index] = 0
            stone_putable_pos.append(index)
    return board, stone_putable_pos


def get_initial_status():
    """
    get initial status
    :return: initial_board: list(int)
        shape = (1,64)
    :return:player_color(int)
        1 -> white
        -1 -> black(preceding player)
    """
    player_color = random.choice([-1, 1])
    reversi_packages = ReversiPackages(
        board=None,
        options=None
    )
    return reversi_packages.get_board_status_filled_with_2(player_color), player_color


def step(board, stone_putted_index, player):
    """
    get next state of the board from current board state
    :param board:list(int)
                shape=(1,64)
    :param stone_putted_index:int
    :param player:int
        -1 -> black
        1 -> white

    :return:board(board after action)
    :return:player(next_player)
        -1 -> black
        1 -> white
    :return:game finish flag:
            -1 -> this player loose
            0 -> game is not end yet
            1 -> this player win
            2 -> draw
    """
    "board "
    if board:
        for index in range(len(board)):
            if board[index] == 2:
                board[index] = 0

    reversi_packages = ReversiPackages(
        board=board,
        options=None
    )
    opponent_player = -1 * player
    stone_putable_pos_list = reversi_packages.get_stone_putable_pos(player)
    if stone_putted_index not in stone_putable_pos_list:
        return None, None, -1
    else:
        reversi_packages.reversing_stones(stone_putted_index, player)
        if reversi_packages.get_stone_putable_pos(opponent_player):
            return reversi_packages.get_board_status_filled_with_2(opponent_player), opponent_player, 0
        elif reversi_packages.get_stone_putable_pos(player):
            return reversi_packages.get_board_status_filled_with_2(player), player, 0
        else:
            if player == reversi_packages.check_winner():
                return None, None, 1
            elif player == -1 * reversi_packages.check_winner():
                return None, None, -1
            else:
                return None, None, 2