from signal import Signal, SingleSignal
from typing import List
import numpy as np

investment_options = ["A", "B", "C"]
L = [0, 0, 0]


def set_success_probabilities(probabilities: List[float]):
    """Sets the success probabilities for investment options A, B, C"""
    p_urn_pos = probabilities
    x = p_urn_pos[0]
    y = p_urn_pos[1]
    z = p_urn_pos[2]

    a = [x, x, y, y, z, z]
    b = [y, z, x, z, x, y]
    c = [z, y, z, x, y, x]

    global L
    L = [a, b, c]


def λ(i: int, ω: int):
    """λ(i,ω): Success probability for investment option i and state ω"""
    return L[i][ω]


def 𝜎(γ: Signal, i: int):
    """𝜎(γ,i): Amount of successful signals for investment option i"""
    return γ.signal_combinations[i]


def 𝜂(γ: Signal):
    """𝜂(γ,i): Amount of information acquisitions"""
    return γ.amount_info


def prior(ω: int):
    """p(ω): Prior belief about ω"""
    return 1 / 6


def p_γ_given_ω(γ: Signal, ω: int):
    """p(γ|ω): Probability for signal combination 𝛾 given state 𝜔"""
    product = 1
    for i in 0, 1, 2:
        product *= λ(i, ω) ** 𝜎(γ, i)
        product *= (1 - λ(i, ω)) ** (𝜂(γ) - 𝜎(γ, i))
    # print("p({}|ω={}) = {}".format(γ.notation(), ω+1, product))
    return product


def p(γ: Signal):
    """p(γ): Probability for signal combination 𝛾"""
    sum = 0
    for ω in range(0, 6):
        sum += p_γ_given_ω(γ, ω) * prior(ω)
    # print("p({}) = {}".format(γ.notation(), sum))
    return sum


def p_s_given_γ(s: SingleSignal, γ: Signal):
    """p(γ): Probability for single signal s given previous signal combination 𝛾"""
    sum = 0
    for ω in range(0, 6):
        sum += posterior(ω, γ) * p_γ_given_ω(s, ω)
    # print("p({}|{}) = {}".format(s.notation(), γ.notation(), sum))
    return sum


def posterior(ω: int, γ: Signal):
    """p(ω|γ): Posterior (Bayes' Rule)"""
    value = p_γ_given_ω(γ, ω) * prior(ω) / p(γ)
    # print("p(ω={}|{}) = {}".format(ω + 1, γ.notation(), value))
    return value


def u(i: int, ω: int):
    """u(i(ω): Utility function"""
    return λ(i, ω) * Z_R


def G_γ_i(γ: Signal, i: int):
    """G(γ,i): Expected gross profit of investment option i and signal combination γ received"""
    sum = 0
    for ω in range(0, 6):
        sum += posterior(ω, γ) * u(i, ω)
    # print("G(γ,{}) = {}".format(i, sum))
    return sum


def G(γ: Signal):
    """G(γ): Expected gross profit for signal combination γ received (assuming optimal behaviour)"""
    gross_profits = []
    for i in 0, 1, 2:
        gross_profits.append(G_γ_i(γ, i))
    print("G({}) = {} (→ {})".format(γ.notation(),
                                     max(gross_profits),
                                     investment_options[np.argmax(gross_profits)]))

    return max(gross_profits)


def F(γ: Signal):
    """F(γ): Expected average future gross profit if an additional single single is acquired"""
    sum = 0
    for i in range(0, 8):
        s = SingleSignal([(i // 4) % 2, (i // 2) % 2, i % 2])
        sum += p_s_given_γ(s, γ) * G(γ + s)
    print("F({}) = {}".format(γ.notation(), sum))
    return sum


Z_R = 1200  # Profit of successful investment
set_success_probabilities([0.9, 0.5, 0.1])
s1 = Signal([2, 1, 1], 2)
diff = F(s1) - G(s1)
print("F(γ) - G(γ) = {}".format(diff))
