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
screen_width, screen_height = 1400, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Train Simulation")
background_color = (30, 30, 30)
clock = pygame.time.Clock()
fps = 60

vsm = default_vsm()

font = pygame.font.Font(None, 24)

# Добавим эти переменные глобально
wait_data = []
run_data = []
repair_data = []
time_data = []
update_time = 0  # Временная метка для графиков




def draw_graph(screen, data, title, position, color, max_points=100):
    font = pygame.font.Font(None, 24)
    graph_width, graph_height = 300, 150  # Увеличенный размер для графика
    origin = (position[0], position[1] + graph_height)  # Нижняя левая точка для графика

    # Отрисовка заголовка графика
    title_surf = font.render(title, True, (255, 255, 255))
    screen.blit(title_surf, (position[0], position[1] - 30))

    # Проверка наличия данных
    if len(data) < 2:
        return

    # Настройка масштаба данных
    max_value = max(data) if max(data) > 0 else 1
    min_value = min(data) if min(data) < max_value else 0
    data_scaled = [(y - min_value) / (max_value - min_value) * graph_height for y in data]

    # Отрисовка графика
    for i in range(1, len(data)):
        start_pos = (origin[0] + (i - 1) * (graph_width / max_points), origin[1] - data_scaled[i - 1])
        end_pos = (origin[0] + i * (graph_width / max_points), origin[1] - data_scaled[i])
        pygame.draw.line(screen, color, start_pos, end_pos, 2)

    # Отрисовка осей
    pygame.draw.line(screen, (255, 255, 255), origin, (origin[0] + graph_width, origin[1]), 2)  # ось X
    pygame.draw.line(screen, (255, 255, 255), origin, (origin[0], origin[1] - graph_height), 2)  # ось Y

    # Метки на осях
    for i in range(0, max_value + 1, max(1, max_value // 10)):
        label = font.render(str(i), True, (255, 255, 255))
        screen.blit(label, (origin[0] - 30, origin[1] - (i - min_value) / (max_value - min_value) * graph_height - 10))

    # Отрисовка сетки
    for i in range(10):  # 10 линий сетки по оси X
        x = origin[0] + i * (graph_width / 10)
        pygame.draw.line(screen, (100, 100, 100), (x, origin[1]), (x, origin[1] - graph_height), 1)
    for i in range(0, max_value + 1, max(1, max_value // 10)):  # Линии сетки по оси Y
        y = origin[1] - (i / max_value) * graph_height
        pygame.draw.line(screen, (100, 100, 100), (origin[0], y), (origin[0] + graph_width, y), 1)


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
    global update_time, wait_data, run_data, repair_data, time_data
    running = True
    timer = 0
    update_interval = 50  # m
    graph_update_interval = update_interval# s


    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)
        timer += clock.get_time()
        if timer > update_interval:
            print(vsm.step_hour())

            timer %= update_interval

        if current_time - update_time > graph_update_interval:

            num_wait = len([train for train in vsm.trains if train.state == 'wait'])
            num_run = len([train for train in vsm.trains if train.state == 'run'])
            num_repair = len([train for train in vsm.trains if train.state == 'repair'])

            wait_data.append(num_wait)
            run_data.append(num_run)
            repair_data.append(num_repair)

            time_data.append(current_time // 1000 - origin_time.timestamp() // 1000)
            update_time = current_time

            decris = 100
            if len(time_data) > decris:  # Ограничение размера данных для графика
                wait_data = wait_data[-decris:]
                run_data = run_data[-decris:]
                repair_data = repair_data[-decris:]
                time_data = time_data[-decris:]

        wait_trains = [train for train in vsm.trains if train.state == 'wait']
        run_trains = sorted([train for train in vsm.trains if train.state == 'run'], key=lambda x: x.run_t)
        repair_trains = sorted([train for train in vsm.trains if train.state == 'repair'], key=lambda x: x.repair_t)

        screen.fill((0,0,0))
        title_surf = font.render(f'Дата: {vsm.current_date()}', True, (255, 200, 255))
        screen.blit(title_surf, (50, 10))



        draw_table(screen, wait_trains, "Waiting Trains", (50, 100), (100, 100, 100), (255, 255, 255))
        draw_table(screen, run_trains, "Running Trains", (300, 100), (100, 255, 100), (255, 255, 255))
        draw_table(screen, repair_trains, "Repairing Trains", (550, 100), (255, 100, 100), (255, 255, 255))

        draw_graph(screen, wait_data, "Wait State Over Time", (850, 50), (100, 100, 255))
        draw_graph(screen, run_data, "Run State Over Time", (850, 250), (100, 255, 100))
        draw_graph(screen, repair_data, "Repair State Over Time", (850, 450), (255, 100, 100))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
