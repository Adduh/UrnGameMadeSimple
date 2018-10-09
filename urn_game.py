from signal import Signal, SingleSignal
from typing import List

import numpy as np

investment_options = ["A", "B", "C"]


class UrnGame:
    def __init__(self, urn_probabilities: List[float], success_profit: float):
        self._Z_R = success_profit
        self._set_success_probabilities(urn_probabilities)

    def _set_success_probabilities(self, urn_probabilities: List[float]):
        """Sets the success probabilities for investment options A, B, C"""
        x, y, z = urn_probabilities
        a = [x, x, y, y, z, z]
        b = [y, z, x, z, x, y]
        c = [z, y, z, x, y, x]
        self._L = [a, b, c]

    def _λ(self, i: int, ω: int):
        """λ(i,ω): Success probability for investment option i and state ω"""
        return self._L[i][ω]

    def _p_γ_given_ω(self, γ: Signal, ω: int):
        """p(γ|ω): Probability for signal combination 𝛾 given state 𝜔"""
        product = 1
        for i in 0, 1, 2:
            product *= self._λ(i, ω) ** 𝜎(γ, i)
            product *= (1 - self._λ(i, ω)) ** (𝜂(γ) - 𝜎(γ, i))
        # print("p({}|ω={}) = {}".format(γ.notation(), ω+1, product))
        return product

    def _p(self, γ: Signal):
        """p(γ): Probability for signal combination 𝛾"""
        sum = 0
        for ω in range(0, 6):
            sum += self._p_γ_given_ω(γ, ω) * prior(ω)
        # print("p({}) = {}".format(γ.notation(), sum))
        return sum

    def _p_s_given_γ(self, s: SingleSignal, γ: Signal):
        """p(γ): Probability for single signal s given previous signal combination 𝛾"""
        sum = 0
        for ω in range(0, 6):
            sum += self._posterior(ω, γ) * self._p_γ_given_ω(s, ω)
        # print("p({}|{}) = {}".format(s.notation(), γ.notation(), sum))
        return sum

    def _posterior(self, ω: int, γ: Signal):
        """p(ω|γ): Posterior (Bayes' Rule)"""
        value = self._p_γ_given_ω(γ, ω) * prior(ω) / self._p(γ)
        # print("p(ω={}|{}) = {}".format(ω + 1, γ.notation(), value))
        return value

    def _u(self, i: int, ω: int):
        """u(i(ω): Utility function"""
        return self._λ(i, ω) * self._Z_R

    def _G_γ_i(self, γ: Signal, i: int):
        """G(γ,i): Expected gross profit of investment option i and signal combination γ received"""
        sum = 0
        for ω in range(0, 6):
            sum += self._posterior(ω, γ) * self._u(i, ω)
        # print("G(γ,{}) = {}".format(i, sum))
        return sum

    def G(self, γ: Signal):
        """G(γ): Expected gross profit for signal combination γ received (assuming optimal behaviour)"""
        gross_profits = []
        for i in 0, 1, 2:
            gross_profits.append(self._G_γ_i(γ, i))
        # print("G({}) = {} (→ {})".format(γ.notation(),
        #                                  max(gross_profits),
        #                                  investment_options[np.argmax(gross_profits)]))
        return max(gross_profits), gross_profits

    def F(self, γ: Signal):
        """F(γ): Expected average future gross profit if an additional single single is acquired"""
        sum = 0
        for i in range(0, 8):
            s = SingleSignal([(i // 4) % 2, (i // 2) % 2, i % 2])
            g, _ = self.G(γ + s)
            sum += self._p_s_given_γ(s, γ) * g
        # print("F({}) = {}".format(γ.notation(), sum))
        return sum


def 𝜎(γ: Signal, i: int):
    """𝜎(γ,i): Amount of successful signals for investment option i"""
    return γ.signal_combinations[i]


def 𝜂(γ: Signal):
    """𝜂(γ,i): Amount of information acquisitions"""
    return γ.amount_info


def prior(ω: int):
    """p(ω): Prior belief about ω"""
    return 1 / 6
