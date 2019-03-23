import copy

import numpy as np
import toml


class ReversiPackages(object):
    '''
    This class is packages used in reversi_processor.py
    '''

    def __init__(self, board=None, options=None, display_board=True):

        '''
        Initialize class parameters.
        
        Args:
            display_board(boolean):
                False -> not display board
                True -> display board

            board(list):
                shape = (total_square_num=64, 1)
                instructions: board state
                              empty(no stone) -> 0
                              white stone -> 1
                              brack stone -> -1

            options(toml):
                global parameters.
        '''

        # self.__options is global parameters
        if options == None:
            # self.__options = toml.load('./reversiAPI/utils/settings.toml')['REVERSI_PACKAGES']
            self.__options = toml.load('./utils/settings.toml')['REVERSI_PACKAGES']
        else:
            self.__options = options

        # self.__board is game board
        if board == None:
            self.__board = []

            # make empty board.
            for index in range(self.__options['SQUARE_NUM']):
                self.__board.append(self.__options['EMPTY'])

            # set initial 2 white stones
            for initial_white_place in self.__options['INITIAL_WHITE_PLACES']:
                self.__board[initial_white_place] = self.__options['WHITE']

            # set initial 2 black stones
            for initial_black_place in self.__options['INITIAL_BLACK_PLACES']:
                self.__board[initial_black_place] = self.__options['BLACK']

        else:
            self.__board = board

        # self.__winner flag is used when checking __winner
        self.__winner = None

        # self.__reversible_stone_number_dict: dictionary
        #   keys: empty(no stone) index in game board
        #   values: list of how many stones reversed when putting stone there for all 8 directions
        self.__reversible_stone_number_dict = {}

        self.__display_board = display_board
        # make class variables for displaying board
        if self.__display_board:

            # converter dictinary (1, -1, 0 -> "⚪️", " ⚫️", "None")
            # self.__marks = toml.load('./reversiAPI/utils/settings.toml')['MARKS']
            self.__marks = toml.load('./utils/settings.toml')['MARKS']

            # number board (1 ~ 64) for displaying
            self.__index_board_for_displaying = []
            for index in range(self.__options['SQUARE_NUM']):
                self.__index_board_for_displaying.append(index + 1)

    def _get_index_in_padded_board(self, index_in_1d_board):
        '''
        This function get index in padded 8x8 board from one dimension board index
        Args board:
        Returns:

        '''
        return index_in_1d_board // self.__options['SIDES_NUM'] + 1, index_in_1d_board % self.__options['SIDES_NUM'] + 1

    def _get_reversible_stone_num_loop(self, base_vector, unit_vector, index, padded_board, stone_color, counter):
        '''
         this function get the if the stone is reversible in the index and vector,
         and also get the number of reversible stone

        Args:
            base_vector(list):
                shape = (2,1)
                instruction: base vector

            unit_vector(list):
                shape = (2,1)
                instruction: put unit vector of all direction

            index(int):
                shape = ()
                instruction: index of the empty place in one dimension array which length is 64.

            padded_board(numpy error):
                shape = (10,10)
                instruction: padded Reversi board

            stone_color(int):
                stone's color
                white -> 1
                black -> -1

        Return:
             is_reversible(boolean):
                shape = ()
                instruction:
                    true -> the stone is reversible in this index and vector
                    false -> the stone is not reversible in this index and vector

            count(int):
                shape = ()
                instruction: the number of reversible stone

        '''
        # counter counts the number of reversible stone
        counter += 1

        # status is the status in focused place of this function
        status = padded_board[self._get_index_in_padded_board(index)[0] +
                              base_vector[0]][self._get_index_in_padded_board(index)[1] + base_vector[1]]

        # if status is different to the stone_color, use _get_reversible_stone_num_loop to conclude the count
        if status == self.__options['CHANGE_COLOR'] * stone_color:
            base_vector[0] += unit_vector[0]
            base_vector[1] += unit_vector[1]
            is_reversible, counter = \
                self._get_reversible_stone_num_loop(base_vector, unit_vector, index, padded_board, stone_color, counter)

        # if status is same as the stone_color, return True and counter
        elif status == stone_color:
            is_reversible = True

        # if status is empty or edge, return False to is_reversible
        else:
            is_reversible = False

        return is_reversible, counter

    def _get_reversible_stone_num(self, unit_vector, index, padded_board, stone_color):
        '''
        this function get the if the stone is reversible in the index and vector,
         and also get the number of reversible stone

        Args:
            unit_vector(list):
                shape = (2,1)
                instruction = put unit vector of all direction

            index(int):
                shape = ()
                instruction: index of the empty place in one dimension array which length is 64.

            padded_board(numpy array):
                shape = (10,10)
                instruction: padded Reversi board

            stone_color(int):
                stone's color
                white -> 1
                black -> -1

        Return:
             is_reversible(boolean):
                shape = ()
                instruction:
                    true -> the stone is reversible in this index and vector
                    false -> the stone is not reversible in this index and vector
        '''
        # counter counts the number of reversible stone
        counter = 1

        # status is the status in focused place of this function
        status = padded_board[self._get_index_in_padded_board(index)[0] + 2 *
                              unit_vector[0]][self._get_index_in_padded_board(index)[1] + 2 * unit_vector[1]]

        # if status is different to the stone_color, use _get_reversible_stone_num_loop to conclude the count
        if status == self.__options['CHANGE_COLOR'] * stone_color:
            base_vector = [0, 0]
            base_vector[0] = 3 * unit_vector[0]
            base_vector[1] = 3 * unit_vector[1]
            is_reversible, counter = \
                self._get_reversible_stone_num_loop(base_vector, unit_vector, index, padded_board, stone_color, counter)
        # if status is same as the stone_color, return True and counter
        elif status == stone_color:
            is_reversible = True

        # if status is empty or edge, return False to is_reversible
        else:
            is_reversible = False

        return is_reversible, counter

    def get_stone_putable_pos(self, stone_color):

        '''
        This function get stone putable position from player's stone_color

        Args:
            stone_color(int):
                shape = ()
                instructions:
                              white -> 1
                              brack -> -1

        Returns:
            putable_pos(list):
                shape = (the number of stone putable position)
                instructions:
                    get stone putable position list

        '''

        # change the shape of board list to 2 dimension numpy array
        board_8x8 = np.array(self.__board).reshape(self.__options['SIDES_NUM'], self.__options['SIDES_NUM'])

        # Pad the edges
        vertical_edge_pad = np.full((1, self.__options['SIDES_NUM']), self.__options['EDGE_PAD'])
        horizontal_edge_pad = np.full((self.__options['SIDES_NUM'] + 2, 1), self.__options['EDGE_PAD'])
        vertical_padded_board = np.vstack((vertical_edge_pad, board_8x8, vertical_edge_pad))
        padded_board = np.hstack((horizontal_edge_pad, vertical_padded_board, horizontal_edge_pad))

        empty_pos_index_list = []
        for index in range(self.__options['SQUARE_NUM']):
            if self.__board[index] == self.__options['EMPTY']:
                empty_pos_index_list.append(index)

        # putable_pos_set is a set of stone putable place
        putable_pos_set = set()

        # for every empty place, validate if the stone is putable
        for empty_pos_index in empty_pos_index_list:
            reversible_stone_number_list = copy.deepcopy(self.__options['INITIAL_REVERSIBLE_STONE_NUMBER_LIST'])

            # for every direction from the index, validate if there is the reversible stone
            for index in range(self.__options['VECTOR_NUM']):
                vector = self.__options['ALL_VECTORS'][index]

                # if the place next to index place have the stone which color is different from the player stone color,
                if padded_board[self._get_index_in_padded_board(empty_pos_index)[0] +
                                vector[0]][self._get_index_in_padded_board(empty_pos_index)[1] + vector[1]] == \
                        self.__options['CHANGE_COLOR'] * stone_color:

                    # validate is the stone is reversible by _get_reversible_stone_num
                    is_reversible, counter = \
                        self._get_reversible_stone_num(vector, empty_pos_index, padded_board, stone_color)

                    # if there is reversible stones, save the vector and the number of stones in\
                    # reversible_stone_number_list and save the index in putable_pos_set
                    if is_reversible:
                        reversible_stone_number_list[index] = counter
                        putable_pos_set.add(empty_pos_index)

            # save the empty_pos_index and reversible_stone_number_list in reversible_stone_number_dict to use in\
            # reversing_stones function
            self.__reversible_stone_number_dict[empty_pos_index] = reversible_stone_number_list

        return list(putable_pos_set)

    def check_winner(self):

        '''
        This function check which player wins (black stone player of white stone player) or draw.
            if __winner is white, self.__winner <- 1
            if __winner is brack, self.__winner <- -1
            if draw, self.__winner <- 2
        '''

        sum_score = sum(self.__board)

        # if __winner is white, sum_score > 0
        if sum_score > 0:
            self.__winner = self.__options['WHITE']

        # if __winner is black, sum_score < 0
        elif sum_score < 0:
            self.__winner = self.__options['BLACK']

        # if draw, sum_score = 0
        else:
            self.__winner = self.__options['DRAW']

        return self.__winner

    def reversing_stones(self, putting_index, stone_color):

        '''
        This function reversing stones adapted to putting place.
        inserting reversed board information to self.__board.

        Args:
            putting_index(int):
                index where putting new stone

            stone_color(int):
                stone's color
                white -> 1
                black -> -1
        '''

        # putting new stone
        self.__board[putting_index] = stone_color

        # reversing stone for all 8 directions adapting to self.__reversible_stone_number_dict
        for index in range(self.__options['VECTOR_NUM']):
            vector = self.__options['ALL_VECTORS'][index]
            for i in range(self.__reversible_stone_number_dict[putting_index][index]):
                i += 1
                self.__board[putting_index + (self.__options['SIDES_NUM'] * vector[0] + vector[1]) * i] *= \
                    self.__options['CHANGE_COLOR']

    def get_board_status(self):
        return self.__board
