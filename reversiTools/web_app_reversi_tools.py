import os
import random

import numpy as np
import torch

from reversiTools.utils.dqn_models.models import TheModelClass
from reversiTools.utils.reversi_packages import ReversiPackages
from reversiTools.utils.settings import DQN
from reversiTools.utils.settings import MARKS


def intlist2strings(intlist):
    string_list = list(map(str, intlist))
    return ','.join(string_list)


def strings2intlist(strings):
    string_list = strings.split(',')
    return list(map(int, string_list))


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


def _load_model(file_path):
    model = TheModelClass(65, 128, 64)
    model.load_state_dict(torch.load(file_path))
    model.eval()
    return model


def get_dqn_move(board, player):
    """
    get dqn move index from board, stone color and pt file path
    :param board: list(int)
        shape=(1,64)
    :param stone_color:int
         -1 -> black
        1 -> white
    :return: index(int)
    """

    if board:
        for index in range(len(board)):
            if board[index] == 2:
                board[index] = 0

    reversi_package = ReversiPackages(board=board, options=None)
    executing_file_path = os.path.dirname(os.path.abspath(__file__))
    pt_path = DQN['model1']
    file_path = os.path.join(executing_file_path, pt_path)
    model = _load_model(file_path)
    with torch.no_grad():
        input_array = np.append(
            np.array(player),
            np.array(reversi_package.get_board_status_filled_with_2(player))
        )
        input_data = torch.from_numpy(input_array).type(torch.FloatTensor)
        input_data_unsqueezed = torch.unsqueeze(input_data, 0)
        q_values = np.array(model(input_data_unsqueezed)).reshape(-1)

    putable_index = reversi_package.get_stone_putable_pos(player)
    stone_put_index = putable_index[0]
    for index in putable_index:
        if q_values[stone_put_index] < q_values[index]:
            stone_put_index = index
    return stone_put_index


def intlist2symbol_list(intlist):
    '''
    this function get symbol_list('⚪️','⚫️'," ","☆") from intlist(1,0,-1,2)
    this symbol list is used to show clients reversi board image

    Args:
        intlist(list):
            length = 64
            values = (1, -1, 0, 2)

    Returns:
        symbol_list(list)
            length = 64
            values = ('⚪️','⚫️',str(index),"☆")
    '''
    assert len(intlist) == 64, 'input list length is invalid'

    symbol_list = []
    index_list = [i for i in range(1, 65)]
    for idx, num in enumerate(intlist):
        if num == 0:
            symbol_list.append(str(index_list[idx]).zfill(2))
        else:
            symbol_list.append(MARKS[str(num)])

    return symbol_list


def inc_list(putable_pos):
    """
    plus 1 for all element of putablie pos list
    :param putable_pos:list(int)
    :return:incremented_list:list(int)
    """
    incremented_list = []
    for index in putable_pos:
        incremented_list.append(index + 1)
    return incremented_list
