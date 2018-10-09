from urn_game import UrnGame
from signal import Signal

s1 = Signal([2, 1, 2], 2)
urns = [UrnGame([0.9, 0.5, 0.1], 600), UrnGame([0.9, 0.5, 0.1], 1200),
        UrnGame([0.2, 0.15, 0.1], 600), UrnGame([0.2, 0.15, 0.1], 1200)]

for i in range(0,4):
    print("Variation {}:".format(i+1))
    urn = urns[i]
    g, _ = urn.G(s1)
    diff = urn.F(s1) - g
    print("F(γ) - G(γ) = {}".format(diff))


urn = urns[0]
g, _ = urn.G(s1)
diff = urn.F(s1) - g
print("F(γ) - G(γ) = {}".format(diff))
