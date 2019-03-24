# import unittest
#
# unittest.main()


from reversiTools.web_app_reversi_tools import get_simple_board
from reversiTools.web_app_reversi_tools import step

print(step(None, 19, -1))
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
print(b)

print(get_simple_board(b[0]))
