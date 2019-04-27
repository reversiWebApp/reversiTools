import copy
import os
import random

import numpy as np
import torch

from reversiTools.utils.models.models import TheModelClass
from reversiTools.utils.models.models import TheModelClassSl1
from reversiTools.utils.reversi_packages import ReversiPackages
from reversiTools.utils.settings import MARKS
from reversiTools.utils.settings import MODELS


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
    return_board = copy.deepcopy(board)
    stone_putable_pos = []
    for index in range(len(return_board)):
        if return_board[index] == 2:
            return_board[index] = 0
            stone_putable_pos.append(index)
    return return_board, stone_putable_pos


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
    :return:valid flag(boolean):
        True -> user action  valid
        False -> user action invalid
    """

    if board:
        board = [0 if i == 2 else i for i in board]
    reversi_packages = ReversiPackages(
        board=board,
        options=None
    )
    opponent_player = -1 * player
    stone_putable_pos_list = reversi_packages.get_stone_putable_pos(player)
    if stone_putted_index not in stone_putable_pos_list:
        valid_flag = False
        for index in stone_putable_pos_list:
            board[index] = 2
        return board, player, 0, valid_flag
    else:
        valid_flag = True
        reversi_packages.reversing_stones(stone_putted_index, player)
        if reversi_packages.get_stone_putable_pos(opponent_player):
            return reversi_packages.get_board_status_filled_with_2(opponent_player), opponent_player, 0, valid_flag
        elif reversi_packages.get_stone_putable_pos(player):
            return reversi_packages.get_board_status_filled_with_2(player), player, 0, valid_flag
        else:
            if player == reversi_packages.check_winner():
                return board, player, 1, valid_flag
            elif player == -1 * reversi_packages.check_winner():
                return board, player, -1, valid_flag
            else:
                return board, player, 2, valid_flag


def _load_model(file_path, cp_name):
    if cp_name == 'DQN':
        model = TheModelClass(65, 128, 64)
        model.load_state_dict(torch.load(file_path))
        model.eval()
    elif cp_name == 'SL':
        model = TheModelClassSl1()
        model.load_state_dict(torch.load(file_path))
        model.eval()
    elif cp_name == 'RANDOM':
        model = None
    else:
        raise ValueError('cp_name is not valid')

    return model


def get_cp_move(board, player, cp_name):
    """
    get dqn move index from board, stone color and pt file path
    :param board: list(int)
        shape=(1,64)
    :param player:int
         -1 -> black
        1 -> white
    :param cp_name:str
    :return: index(int)
    """

    if board:
        board = [0 if i == 2 else i for i in board]

    reversi_packages = ReversiPackages(board=board, options=None)
    executing_file_path = os.path.dirname(os.path.abspath(__file__))
    pt_path = MODELS[cp_name]
    file_path = os.path.join(executing_file_path, pt_path)
    model = _load_model(file_path, cp_name)
    putable_index = reversi_packages.get_stone_putable_pos(player)
    if cp_name == 'DQN':
        with torch.no_grad():
            input_array = np.append(
                np.array(player),
                np.array(reversi_packages.get_board_status_filled_with_2(player))
            )
            input_data = torch.from_numpy(input_array).type(torch.FloatTensor)
            input_data_unsqueezed = torch.unsqueeze(input_data, 0)
            q_values = np.array(model(input_data_unsqueezed)).reshape(-1)

        filtered_probability = np.full(64, -100000)
        for index in putable_index:
            filtered_probability[index] = q_values[index]
            stone_put_index = np.argmax(filtered_probability)
            if filtered_probability[stone_put_index] == -100000:
                stone_put_index = putable_index[0]
    if cp_name == 'SL':
        with torch.no_grad():
            input_array = np.array(reversi_packages.get_board_status())

            # 黒手番の時の盤面情報は反転させる
            if player == -1:
                input_array *= -1

            # 推論に使えるデータサイズに変更する
            input_array = input_array.reshape(-1, 1, 8, 8)

            # NNの出力を算出
            input_tensor = torch.Tensor(input_array)
            output = model(input_tensor)
            output = np.array(output[0])

        # 置ける場所のうち最大のindexに石を置く

        filterd_probability = np.full(64, -1000)
        filterd_probability[putable_index] = output[putable_index]
        stone_put_index = np.argmax(filterd_probability)
    if cp_name == 'RANDOM':
        stone_put_index = random.choice(putable_index)
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
            values = ('⚪','⚫',str(index),"☆")
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
    :return incremented_list:list(int)
    """
    incremented_list = []
    for index in putable_pos:
        incremented_list.append(index + 1)
    return incremented_list


def count_stone(board):
    """
    count the number of white stone and black stone
    :param board: list(int)
    :return the number of white stone:int
    :return the number of black stone:int
    """
    return int(board.count(ReversiPackages['WHITE'])), int(board.count(ReversiPackages['BLACK']))
