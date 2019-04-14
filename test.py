# import unittest
#
# unittest.main()


from reversiTools.ml_reversi_tools import get_stone_putable_pos
from reversiTools.web_app_reversi_tools import get_dqn_move
from reversiTools.web_app_reversi_tools import get_simple_board
from reversiTools.web_app_reversi_tools import step
from reversiTools.web_app_reversi_tools import intlist2symbol_list

print(len(step(None, 19, -1)[0]))
a = []
for _ in range(16):
    a.append(0)
for _ in range(16):
    a.append(1)
for _ in range(16):
    a.append(-1)
for _ in range(16):
    a.append(0)
b = step(a, 14, -1)
print(len(b[0]))

print(len(get_simple_board(b[0])))

dqn_index = get_dqn_move(a, -1)
print(dqn_index)
print(get_stone_putable_pos(a, -1))

input_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        1, 0, -1, 2, 1, 0, -1, 2, 1, 0, -1, 2,
        1, 0, -1, 2, 1, 0, -1, 2, 1, 0, -1, 2
        ]
print(intlist2symbol_list(input_list))
