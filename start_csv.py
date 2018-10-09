import math
import pandas as pd
import numpy as np

from signal import Signal, SingleSignal
from urn_game import UrnGame

csv_file = "stataforpython.csv"
data = pd.read_csv(csv_file).to_dict(orient="row")

cols = ["game_id"]

for i in range(0, 9):
    cols.append("exp_{}".format(i))
    cols.append("avg_{}".format(i))
    cols.append("diff_{}".format(i))

cols.append("end_exp_a")
cols.append("end_exp_b")
cols.append("end_exp_c")
cols.append("end_max_exp_urn")
cols.append("optexit_urn")
cols.append("optexit")
cols.append("optimal")

data_rows = []
investment_options = ["A", "B", "C"]


def append_per_signal(row: dict, signal_count: int, f: float, g: float, success_profit: float, cost: int):
    row['exp_{}'.format(signal_count)] = g / success_profit
    row['avg_{}'.format(signal_count)] = f / success_profit
    row['diff_{}'.format(signal_count)] = f - g - cost


for n, input in enumerate(data, 1):
    # print('Game {} (game_id: {} {}):'.format(n, input['game_id'], [input['a'], input['b'], input['c']]))
    output = {'game_id': int(input['game_id'])}
    signal = Signal()

    urn = UrnGame([input['a'], input['b'], input['c']], input['succinv'])
    g, gross_profits = urn.G(signal)
    f = urn.F(signal)
    append_per_signal(output, 0, f, g, input['succinv'], input['directcostaddinfo'])

    optimal_exit_roll_count = 0
    optimal_exit_max_exp_pos = -1
    optimal_exit_roll_count_found = False
    current_roll = 0
    if not optimal_exit_roll_count_found:
        if f - g - input['directcostaddinfo'] > 0:
            optimal_exit_roll_count = current_roll + 1
            optimal_exit_max_exp_pos = np.argmax(gross_profits)
        else:
            optimal_exit_roll_count_found = True
    option = int(input['option']) - 1
    for signal_position in range(1, 9):
        label = 'signal{}'.format(signal_position)
        if math.isnan(input[label]):
            continue
        current_roll += 1

        signal += Signal.from_number(int(input[label]))
        g, gross_profits = urn.G(signal)
        f = urn.F(signal)
        append_per_signal(output, signal_position, f, g, input['succinv'], input['directcostaddinfo'])
        if not optimal_exit_roll_count_found:
            if f - g - input['directcostaddinfo'] > 0:
                optimal_exit_roll_count = current_roll + 1
                optimal_exit_max_exp_pos = np.argmax(gross_profits)
            else:
                optimal_exit_roll_count_found = True

    output['end_exp_a'] = gross_profits[0] / input['succinv']
    output['end_exp_b'] = gross_profits[1] / input['succinv']
    output['end_exp_c'] = gross_profits[2] / input['succinv']
    output['end_max_exp_urn'] = investment_options[np.argmax(gross_profits)]
    output['optexit'] = optimal_exit_roll_count
    output['optexit_urn'] = investment_options[optimal_exit_max_exp_pos]
    was_actual_choice_optimal = 1 if output['end_max_exp_urn'] == investment_options[option] else 0
    exp_pos = [output['end_exp_a'], output['end_exp_b'], output['end_exp_c']]
    diff = exp_pos[np.argmax(gross_profits)] - exp_pos[option]
    if diff < 10 ** -9:
        was_actual_choice_optimal = 1
    output['optimal'] = was_actual_choice_optimal
    data_rows.append(output.copy())

# for dr in data_rows:
#     print(dr)

df = pd.DataFrame(data=data_rows, columns=cols)

df.to_csv("export.csv")
