# import unittest
#
# unittest.main()


from reversiTools.ml_reversi_tools import step

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

print(step(a, 16, -1))
