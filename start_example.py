from urn_game import UrnGame
from signal import Signal

urn = UrnGame([0.9, 0.5, 0.1], 1200)
s1 = Signal([2, 1, 1], 2)
g, _ = urn.G(s1)
diff = urn.F(s1) - g
print("F(γ) - G(γ) = {}".format(diff))
