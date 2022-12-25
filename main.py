import os
import time
import curses
import asyncio
import random
from animation import fire, animate_spaceship

TIC_TIMEOUT = 0.1


def fire_draw(canvas):
    curses.curs_set(False)
    canvas.border()
    height, width = canvas.getmaxyx()
    coroutine = fire(canvas, height / 2, width / 2)
    while True:
        try:
            coroutine.send(None)
        except StopIteration:
            break
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)
    height, width = canvas.getmaxyx()
    with open(os.path.join(os.getcwd(), 'frames', ' rocket_frame_1.txt'), 'r', encoding='utf-8') as file:
        frame1 = file.read()
    with open(os.path.join(os.getcwd(), 'frames', ' rocket_frame_2.txt'), 'r', encoding='utf-8') as file:
        frame2 = file.read()
    coroutines = [animate_spaceship(canvas, height / 3, width / 2, frame1, frame2)]
    for _ in range(300):
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        symbol = random.choice('+*.:')
        coroutines.append(blink(canvas, row, column, symbol))
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


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        d = random.randint(0, 5)
        for _ in range(d + 20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(d + 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(d + 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(d + 3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(fire_draw)
    curses.wrapper(draw)
