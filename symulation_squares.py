from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

from train import default_vsm

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

vsm = default_vsm()

font = pygame.font.Font(None, 24)

def draw_table(screen, trains, title, top_left, table_color, text_color):
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

def main():
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
        repair_trains = sorted([train for train in vsm.trains if train.state == 'repair'], key=lambda x: x.repair_t)

        screen.fill((0,0,0))
        title_surf = font.render(f'Дата: {vsm.current_date()}', True, (255, 200, 255))
        screen.blit(title_surf, (50, 10))

        draw_table(screen, wait_trains, "Waiting Trains", (50, 100), (100, 100, 100), (255, 255, 255))
        draw_table(screen, run_trains, "Running Trains", (300, 100), (100, 255, 100), (255, 255, 255))
        draw_table(screen, repair_trains, "Repairing Trains", (550, 100), (255, 100, 100), (255, 255, 255))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
