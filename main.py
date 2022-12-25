import time
import curses
import asyncio
import random
from fire_animation import fire
from curses_tools import draw_frame

TIC_TIMEOUT = 0.05


async def animate_spaceship(canvas):
    pass


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
    height, width = canvas.getmaxyx()
    coroutines = []
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


# def star(canvas):
#     curses.curs_set(False)
#     row, column = (5, 20)
#     canvas.border()
#     while True:
#         canvas.addstr(row, column, '*', curses.A_DIM)
#         canvas.refresh()
#         time.sleep(2)
#         canvas.addstr(row, column, '*')
#         canvas.refresh()
#         time.sleep(0.3)
#         canvas.addstr(row, column, '*', curses.A_BOLD)
#         canvas.refresh()
#         time.sleep(0.5)
#         canvas.addstr(row, column, '*')
#         canvas.refresh()
#         time.sleep(0.3)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        d = random.randint(1, random.randint(10, 50))
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
