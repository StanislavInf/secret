from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from typing import List, Tuple

origin_time = datetime.strptime('2024-04-17', '%Y-%m-%d')

class TrainSimulation:

    def __init__(self, tuda_syuda_distance: int, tuda_syuda_hours: int, cycles: List[Tuple[str, int, int, int]]):
        self.tuda_syuda_distance = tuda_syuda_distance
        self.tuda_syuda_hours = tuda_syuda_hours
        self.cycles = cycles

        self.probegs = [0 for _ in cycles]
        self.ts = [0 for _ in cycles]
        self.repair_t = 0
        self.run_t = 0
        self.state = 'wait'
        self.repair_cycle_name = ''

    def step(self):
        if self.state != 'repair':
            for i in range(len(self.ts)):
                self.ts[i] += 1

        if self.state == 'run':
            self.run_t += 1
            if self.run_t == self.tuda_syuda_hours:
                self.state = 'wait'
                self.run_t = 0
                for i in range(len(self.probegs)):
                    self.probegs[i] += self.tuda_syuda_distance

                for i in reversed(range(len(self.cycles))):
                    cycle = self.cycles[i]
                    # ставим на ремонт если доза 90%
                    p = cycle[1] - cycle[1] // 10
                    t = cycle[2] - cycle[2] // 10
                    if self.probegs[i] >= p or self.ts[i] >= t:
                        self.state = 'repair'
                        self.repair_t = cycle[3]
                        self.repair_cycle_name = cycle[0]

                        for j in range(i+1):
                            self.ts[j] = 0
                            self.probegs[j] = 0
                        break

        elif self.state == 'repair':
            self.repair_t -= 1
            if self.repair_t == 0:
                self.state = 'wait'

        return self.state

    def print(self):
        print(self.state, self.probegs, self.ts, end=' ')
        if self.state == 'wait':
            print()
        elif self.state == 'repair':
            print(f'repair={self.repair_t} cycle={self.repair_cycle_name}')
        elif self.state == 'run':
            print(f'run={self.run_t}')

tuda_syuda_distance = 1400
tuda_syuda_hours = 7
cycles = [
    ("IS100", 12500,   7*24,    1),
    ("IS200", 25000,   14*24,   4),
    ("IS510", 75000,   45*24,   6),
    ("IS520", 150000,  90*24,   9),
    ("IS530", 300000,  150*24,  19),
    ("IS540", 600000,  330*24,  28),
    ("IS600", 1200000, 630*24,  192),
    ("IS700", 2400000, 1260*24, 288)
]

class VSM_Station:

    def __init__(self, num_trains: int, max_repair_at_time: int, train_capacity: int, options):
        self.trains = [TrainSimulation(**options) for _ in range(num_trains)]
        self.max_repair_at_time = max_repair_at_time
        self.hour = 0
        self.passenger_distribution = np.ones(24)/24
        self.train_capacity = train_capacity

        self.history = []

    def step_hour(self, num_passengers: int):
        num_repairing_ = 0

        h = self.hour % 24
        passengers = int(self.passenger_distribution[h]*num_passengers)//2
        num_needed_trains = (passengers + self.train_capacity - 1) // self.train_capacity

        for i, train in enumerate(self.trains):

            # не чиним поезда, которые не влезают в ремонтный цех
            if train.state == 'repair' and num_repairing_ >= self.max_repair_at_time:
                continue

            train.step()

            if train.state == 'repair':
                num_repairing_ += 1
            elif train.state == 'wait' and num_needed_trains > 0:
                # print(i)
                train.state = 'run'
                num_needed_trains -= 1
        if num_needed_trains != 0:
            print(f'Passengers left! {num_needed_trains}*{self.train_capacity}={num_needed_trains*self.train_capacity}')

        self.hour += 1
        num_repairin = sum([1 for train in self.trains if train.state=='repair'])
        num_waitin = sum([1 for train in self.trains if train.state=='wait'])
        num_runin = sum([1 for train in self.trains if train.state=='run'])
        self.history.append((num_runin, num_waitin, num_repairin))
        return num_runin, num_waitin, num_repairin

    def save_history(self, path: str, starttime):
        hist = np.array(self.history)
        df = pd.DataFrame({
            'time': [starttime+timedelta(hours=h) for h in range(self.hour)],
            'running': hist[:, 0],
            'waiting': hist[:, 1],
            'repairing': hist[:, 2]
        })
        df.to_excel(path)
        print(f'Saved train history to {path}')

vsm = VSM_Station(num_trains=33, max_repair_at_time=8, train_capacity=450, options={
    'tuda_syuda_distance': 1400,
    'tuda_syuda_hours': 7,
    'cycles': cycles
})

passengers_per_month = [
    16319,                      # jan
    16319,                      # feb
    16319,                      # mar
    16319,                      # apr
    26319,                      # may
    16319,                      # jun
    16319,                      # jul
    16319,                      # aug
    16319,                      # sep
    16319,                      # oct
    16319,                      # nov
    16319                       # dec
]

print('  Num running        Num waiting        Num repairing')
for i in range(9600):
    curr_month = (origin_time + timedelta(hours=vsm.hour)).month

    run, wait, repair = vsm.step_hour(num_passengers=passengers_per_month[curr_month-1])

    if i % 1 == 0:
        print(f'{vsm.hour:4d} {run:5d}              {wait:5d}               {repair:5d}')

vsm.save_history('history.xlsx', origin_time)
