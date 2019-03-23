from reversiTools.utils.reversi_packages import ReversiPackages


def step(board, stone_putted_index, player):
    """
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
    reversi_packages = ReversiPackages(
        board=board,
        options=None,
        display_board=None
    )
    opponent_player = -1 * player
    stone_putable_pos_list = reversi_packages.get_stone_putable_pos(player)
    if stone_putted_index not in stone_putable_pos_list:
        return None, None, -1
    else:
        reversi_packages.reversing_stones(stone_putted_index, player)
        if reversi_packages.get_stone_putable_pos(opponent_player):
            return reversi_packages.get_board_status(), opponent_player, 0
        elif reversi_packages.get_stone_putable_pos(player):
            return reversi_packages.get_board_status(), player, 0
        else:
            if player == reversi_packages.check_winner():
                return None, None, 1
            elif player == -1 * reversi_packages.check_winner():
                return None, None, -1
            else:
                return None, None, 2


def reset():
    """
    :return: initial_board: list(int)
        shape = (1,64)
    :return: preceding player(int) = -1(black)
    """
    reversi_packages = ReversiPackages(
        board=None,
        options=None,
        display_board=None
    )
    return reversi_packages.get_board_status(), -1
