# import unittest
#
# unittest.main()


from reversiTools.ml_reversi_tools import get_stone_putable_pos
from reversiTools.web_app_reversi_tools import get_cp_move
from reversiTools.web_app_reversi_tools import get_simple_board
from reversiTools.web_app_reversi_tools import inc_list
from reversiTools.web_app_reversi_tools import intlist2symbol_list
from reversiTools.web_app_reversi_tools import step


a = []
for _ in range(19):
    a.append(0)
a.append(-1)
a.append(1)
for _ in range(6):
    a.append(0)
a.append(-1)
a.append(1)
for _ in range(6):
    a.append(0)
a.append(-1)
a.append(1)
for _ in range(27):
    a.append(0)
b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, -1, 2, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 2, -1, 1,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(b[21])
print(step(b, 21, -1))

b = step(a, 14, -1)
print(len(b[0]))
print('step:{}'.format(b))



print(len(get_simple_board(b[0])))

dqn_index = get_cp_move(a, -1, 'SL')
print('SL:{}'.format(dqn_index))
print('DQN:{}'.format(get_cp_move(a, -1, 'DQN')))
print('RANDOM:{}'.format(get_cp_move(a, -1, 'RANDOM')))
print(get_stone_putable_pos(a, -1))

input_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              1, 0, -1, 2, 1, 0, -1, 2, 1, 0, -1, 2,
              1, 0, -1, 2, 1, 0, -1, 2, 1, 0, -1, 2
              ]
print(intlist2symbol_list(input_list))

print(inc_list([1, 3, 4, 5, 5, 6, 92, 2354]))
