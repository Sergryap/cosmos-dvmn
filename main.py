import os
import time
import curses
import asyncio
import random
from animation import fire, animate_spaceship, fly_garbage, get_fly_garbage_flow
from animation import MIN_COORD
from obstacles import show_obstacles

TIC_TIMEOUT = 0.1
NUMBER_OF_STARS = 300
MAX_OFFSET_TICS = 5
TRASH_INDEX_DENSITY = 15
MIN_TRASH_SPEED = 0.5
MAX_TRASH_SPEED = 1.0


def run_coroutines(canvas, coroutines):
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)
    rows_number, column_number = canvas.getmaxyx()
    start_rocket_row = rows_number / 3
    start_rocket_col = column_number / 2
    rockets, trashes = [], []
    for folder in os.listdir('frames'):
        path = os.path.join(os.getcwd(), 'frames', folder)
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r', encoding='utf-8') as frame:
                if folder == 'rocket':
                    rockets.append(frame.read())
                elif folder == 'trash':
                    trashes.append(frame.read())
    coroutine_trash_count = column_number // TRASH_INDEX_DENSITY
    coroutines, obstacles = [], []
    coroutines += get_fly_garbage_flow(
            canvas,
            coroutine_trash_count,
            coroutines,
            trashes=trashes,
            min_speed=MIN_TRASH_SPEED,
            max_speed=MAX_TRASH_SPEED,
            obstacles=obstacles
        )
    coroutines.append(show_obstacles(canvas, obstacles))
    for _ in range(NUMBER_OF_STARS):
        row = random.randint(MIN_COORD, rows_number - 2)
        column = random.randint(MIN_COORD, column_number - 2)
        symbol = random.choice('+*.:')
        offset_tics = random.randint(0, MAX_OFFSET_TICS)
        coroutines.append(blink(canvas, row, column, offset_tics, symbol))
    coroutines.append(animate_spaceship(canvas, start_rocket_row, start_rocket_col, coroutines, *rockets))
    run_coroutines(canvas, coroutines)


async def blink(canvas, row, column, offset_tics, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(offset_tics, 20)

        canvas.addstr(row, column, symbol)
        await sleep(offset_tics, 3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(offset_tics, 5)

        canvas.addstr(row, column, symbol)
        await sleep(offset_tics, 3)


async def sleep(offset_tics, tics):
    for _ in range(offset_tics + tics):
        await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

