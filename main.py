import os
import time
import curses
import asyncio
import random
from animation import fire, animate_spaceship, fly_garbage
from animation import MIN_COORD

TIC_TIMEOUT = 0.1
NUMBER_OF_STARS = 300
MAX_OFFSET_TICS = 5


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
    height, width = canvas.getmaxyx()
    rockets, trashes = [], []
    for folder in os.listdir('frames'):
        path = os.path.join(os.getcwd(), 'frames', folder)
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r', encoding='utf-8') as frame:
                if folder == 'rocket':
                    rockets.append(frame.read())
                elif folder == 'trash':
                    trashes.append(frame.read())
    coroutines = [
        fire(canvas, height / 2, width / 2),
        animate_spaceship(canvas, height / 3, width / 2, *rockets),
        fly_garbage(canvas, random.randrange(width), random.choice(trashes), speed=0.5)
    ]

    for _ in range(NUMBER_OF_STARS):
        row = random.randint(MIN_COORD, height - 2)
        column = random.randint(MIN_COORD, width - 2)
        symbol = random.choice('+*.:')
        offset_tics = random.randint(0, MAX_OFFSET_TICS)
        coroutines.append(blink(canvas, row, column, offset_tics, symbol))
    run_coroutines(canvas, coroutines)


async def blink(canvas, row, column, offset_tics, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(offset_tics + 20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(offset_tics + 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(offset_tics + 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(offset_tics + 3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
