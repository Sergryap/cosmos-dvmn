import os
import time
import curses
import asyncio
import random
from animation import fire, animate_spaceship

TIC_TIMEOUT = 0.1


def run_coroutines(canvas, coroutines):
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def start_draw(canvas):
    curses.curs_set(False)
    canvas.border()
    height, width = canvas.getmaxyx()
    coroutines = [fire(canvas, height / 2, width / 2)]
    run_coroutines(canvas, coroutines)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)
    height, width = canvas.getmaxyx()
    frames = []
    for file in os.listdir('frames'):
        with open(os.path.join(os.getcwd(), 'frames', file), 'r', encoding='utf-8') as frame:
            frames.append(frame.read())
    coroutines = [animate_spaceship(canvas, height / 3, width / 2, *frames)]
    for _ in range(300):
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        symbol = random.choice('+*.:')
        coroutines.append(blink(canvas, row, column, symbol))
    run_coroutines(canvas, coroutines)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        time_addition = random.randint(0, 5)
        for _ in range(time_addition + 20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(time_addition + 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(time_addition + 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(time_addition + 3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(start_draw)
    curses.wrapper(draw)
