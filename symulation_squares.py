from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from typing import List, Tuple

import pygame
import sys
import random

origin_time = datetime.strptime('2024-04-17', '%Y-%m-%d')

# Инициализация Pygame
pygame.init()

# Определение констант для размера окна и цветов
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Train Simulation")
background_color = (30, 30, 30)
clock = pygame.time.Clock()
fps = 60

# Определение класса Train
class Train:
    def __init__(self, id_number, distance, hours, cycles):
        self.id_number = id_number
        self.distance = distance
        self.hours = hours
        self.cycles = cycles
        self.probegs = [0] * len(cycles)
        self.ts = [0] * len(cycles)
        self.repair_time = 0
        self.run_time = 0
        self.state = 'wait'

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




class TrainSimulation:

    def __init__(self, id_number, tuda_syuda_distance: int, tuda_syuda_hours: int, cycles):
        self.tuda_syuda_distance = tuda_syuda_distance
        self.tuda_syuda_hours = tuda_syuda_hours
        self.cycles = cycles
        self.id_number = id_number

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

class VSM_Station:

    def __init__(self, num_trains: int, max_repair_at_time: int, train_capacity: int, passenger_distribution_per_hour, passengers_for_months, options):
        self.trains = [TrainSimulation(i, **options) for i in range(num_trains)]
        self.max_repair_at_time = max_repair_at_time
        self.hour = 0
        self.passenger_distribution = passenger_distribution_per_hour
        self.passengers_for_months = passengers_for_months
        self.train_capacity = train_capacity

        self.history = []

    def current_date(self):
        return origin_time + timedelta(hours=self.hour)

    def step_hour(self):
        curr_month = self.current_date().month
        num_passengers = self.passengers_for_months[curr_month-1]

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

    def jump_to_date(self, date):
        curr_date = self.current_date()
        if curr_date > date:
            raise ValueError('Нельзя отмотать время назад')

        hours = (date - curr_date).total_seconds()//3600
        hours = int(hours)
        for _ in range(hours):
            self.step_hour()

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

passenger_distribution_per_hour = np.ones(24)/24

passengers_for_months = [
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

vsm = VSM_Station(num_trains=33, max_repair_at_time=8, train_capacity=450, passenger_distribution_per_hour=passenger_distribution_per_hour, passengers_for_months=passengers_for_months, options={
    'tuda_syuda_distance': 1400,
    'tuda_syuda_hours': 7,
    'cycles': cycles
})

# Функция для отрисовки таблицы с поездами
def draw_table(screen, trains, title, top_left, table_color, text_color):
    font = pygame.font.Font(None, 24)
    title_surf = font.render(title, True, text_color)
    screen.blit(title_surf, (top_left[0], top_left[1] - 30))
    square_size = 40
    padding = 10
    per_row = 5

    for index, train in enumerate(trains):
        row = index // per_row
        col = index % per_row
        x = top_left[0] + (square_size + padding) * col
        y = top_left[1] + (square_size + padding) * row
        pygame.draw.rect(screen, table_color, (x, y, square_size, square_size))
        train_number_surf = font.render(str(train.id_number), True, text_color)
        train_number_rect = train_number_surf.get_rect(center=(x + square_size / 2, y + square_size / 2))
        screen.blit(train_number_surf, train_number_rect)

# Главная функция для запуска игры
def main():
    # Создание списка поездов
    running = True
    timer = 0
    update_interval = 100  # ms

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)
        timer += clock.get_time()
        if timer > update_interval:
            print(vsm.step_hour())

            timer %= update_interval

        wait_trains = [train for train in vsm.trains if train.state == 'wait']
        run_trains = sorted([train for train in vsm.trains if train.state == 'run'], key=lambda x: x.run_t)
        repair_trains = [train for train in vsm.trains if train.state == 'repair']

        screen.fill((0,0,0))

        draw_table(screen, wait_trains, "Waiting Trains", (50, 100), (100, 100, 100), (255, 255, 255))
        draw_table(screen, run_trains, "Running Trains", (300, 100), (100, 255, 100), (255, 255, 255))
        draw_table(screen, repair_trains, "Repairing Trains", (550, 100), (255, 100, 100), (255, 255, 255))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
