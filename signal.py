from typing import List


class Signal:
    def __init__(self, signal_combinations: List[int] = [0, 0, 0], amount_info: int = 0):
        self.signal_combinations = signal_combinations
        self.amount_info = amount_info

    def __add__(self, other):
        amount_info = self.amount_info + other.amount_info
        signal_combinations = [0, 0, 0]
        for i in 0, 1, 2:
            signal_combinations[i] += self.signal_combinations[i] + other.signal_combinations[i]
        return Signal(signal_combinations, amount_info)

    @staticmethod
    def from_number(number: int):
        if number == 1:
            return SingleSignal([1, 1, 1])
        if number == 2:
            return SingleSignal([1, 1, 0])
        if number == 3:
            return SingleSignal([1, 0, 0])
        if number == 4:
            return SingleSignal([0, 0, 0])
        if number == 5:
            return SingleSignal([0, 0, 1])
        if number == 6:
            return SingleSignal([0, 1, 1])
        if number == 7:
            return SingleSignal([1, 0, 1])
        if number == 8:
            return SingleSignal([0, 1, 0])

    def notation(self):
        return "({}{}{})^{}".format(self.signal_combinations[0],
                                    self.signal_combinations[1],
                                    self.signal_combinations[2],
                                    self.amount_info)


class SingleSignal(Signal):
    def __init__(self, signal_combinations: List[int]):
        super().__init__(signal_combinations, 1)

    def notation(self):
        return "({}{}{})".format(self.signal_combinations[0],
                                 self.signal_combinations[1],
                                 self.signal_combinations[2])
