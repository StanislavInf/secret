import matplotlib.pyplot as plt
from typing import List, Tuple

class TrainSimulation:

    def __init__(self, tuda_syuda_distance: int, time_per_tuda_syuda: int, cycles: List[Tuple[str, int, int, int]]):
        self.tuda_syuda_distance = tuda_syuda_distance
        self.time_per_tuda_syuda = time_per_tuda_syuda
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
            if self.run_t == self.time_per_tuda_syuda:
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
time_per_tuda_syuda = 7
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

train = TrainSimulation(tuda_syuda_distance, time_per_tuda_syuda, cycles)
train.state = 'run'
last_state = ''

print('      Train simulation')
print('='*80)
# for i in range(100000):
for i in range(1000):

    if last_state != train.state:
        print(f'{i:4d}| ', end='')
        train.print()
        last_state = train.state

    train.step()
    if train.state == 'wait':
        train.state = 'run'
