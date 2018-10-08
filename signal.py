from typing import List


class Signal:
    def __init__(self, signal_combinations: List[int], amount_info: int):
        self.signal_combinations = signal_combinations
        self.amount_info = amount_info

    def __add__(self, other):
        amount_info = self.amount_info + other.amount_info
        signal_combinations = [0, 0, 0]
        for i in 0, 1, 2:
            signal_combinations[i] += self.signal_combinations[i] + other.signal_combinations[i]
        return Signal(signal_combinations, amount_info)

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
