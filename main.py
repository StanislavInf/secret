from typing import List, Tuple

class TrainSimulation:

    def __init__(self, tuda_syuda_distance: int, time_per_tuda_syuda: int, cycles: List[Tuple[str, int, int, int]]):
        self.tuda_syuda_distance = tuda_syuda_distance
        self.time_per_tuda_syuda = time_per_tuda_syuda
        self.cycles = cycles

        self.probeg = 0
        self.t = 0
        self.remont_t = 0

    def tuda_syuda1(self) -> Tuple[int, int, int]:
        prev_probeg = self.probeg
        self.probeg += self.tuda_syuda_distance
        self.t += self.time_per_tuda_syuda
        for cycle in reversed(cycles):
            if self.probeg % cycle[1] < prev_probeg % cycle[1]:
                self.t += cycle[3]
                self.remont_t += cycle[3]
                break
        return self.probeg, self.t, self.remont_t

    def tuda_syuda2(self) -> Tuple[int, int, int]:
        prev_t = self.t
        self.probeg += self.tuda_syuda_distance
        self.t += self.time_per_tuda_syuda
        for cycle in reversed(cycles):
            if self.t % cycle[2] < prev_t % cycle[2]:
                self.t += cycle[3]
                self.remont_t += cycle[3]
                break
        return self.probeg, self.t, self.remont_t

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

t1 = TrainSimulation(tuda_syuda_distance, time_per_tuda_syuda, cycles)
t2 = TrainSimulation(tuda_syuda_distance, time_per_tuda_syuda, cycles)

print('      Train1                                   Train2')
print('='*60)
for i in range(10):
    print(f'{i:4d}| ', end='')

    p, t, rt = t1.tuda_syuda1()
    print(f'{p:6d} {t:5d} {rt:5d}', end='\t\t\t')

    p, t, rt = t2.tuda_syuda2()
    print(f'{p:6d} {t:5d} {rt:5d}')
